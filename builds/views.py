from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from builds.models import Component, VersionBase, Build, NewBuild
from builds.serializers import ComponentSerializer, VersionBaseSerializer, BuildSerializer, NewBuildSerializer

def get_template_context(request, format):
    context = {
        'builds_handler': reverse('build-list', request=request, format=format),
        'home_url': reverse('index', request=request, format=format),
        'getting_started_url': reverse('getting-started', request=request, format=format),
    }
    return context
@api_view(['GET'])
def index(request, format=None):
    return render(request, 'builds/index.html', get_template_context(request, format))

@api_view(['GET'])
def react(request, format=None):
    return render(request, 'builds/react.html', get_template_context(request, format))

@api_view(['GET'])
def search(request, format=None):
    return Response({
        'message': 'got search'
    })

@api_view(['GET'])
def getting_started(request, format=None):
    return render(request, 'builds/getting_started.html', get_template_context(request, format))

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'builds': reverse('build-list', request=request, format=format),
    })

class ComponentsHandler(APIView):
    """Handles API requests to get all Components that have an associated Build"""

    def get(self, request, format=None):
        components = Component.objects.all()
        serializer = ComponentSerializer(components, many = True)
        return Response(serializer.data)

class VersionsHandler(APIView):
    """ Handles API requests to get all the Versions"""

    def get(self, request, format=None):
        query = VersionBase.objects.all()
        component = request.query_params.get('component', None)
        if component is not None:
            query = query.filter(component__name=component.lower())
        serializer = VersionBaseSerializer(query, many=True)
        return Response(serializer.data)

class BuildsHandler(APIView):
    """Handles API requests to get and create builds."""

    def get(self, request, format=None):
        """Get all the builds in the database"""
        builds = Build.objects.all()
        serializer = BuildSerializer(builds, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """Create a new build.  

        The request data should be able to be deserialized into a NewBuild model.

        """
        serializer = NewBuildSerializer(data=request.data)
        if serializer.is_valid():
            # Create a new build
            build = self.create_build(NewBuild(**serializer.validated_data))

            # Serialize the newly created build to return as the response data
            build_serializer = BuildSerializer(build)
            response = Response(build_serializer.data, status=status.HTTP_201_CREATED)

            # Set the Location header to the URL of the newly created build.  The reverse function
            # looks up a urlpattern by a name.
            response['Location'] = reverse('build', args=[build.pk], request=request, format=format)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create_build(self, new_build):
        """Create a new Build model from a NewBuild instance"""

        # Get/Create the Component model that is associated with this new build.
        # Note that the query is case insensitive on the name.  This way 'VxStorage'
        # and 'vxstorage' will refer to the same Application.
        component, _ = Component.objects.get_or_create(
            name=new_build.component.lower(),
            defaults={'name' : new_build.component.lower()}
        )
        
        # Get/Create the VersionBase model that is associated with the new build.
        version_base, _ = VersionBase.objects.get_or_create(
            value=new_build.version_base,
            component=component,
            defaults={'value' : new_build.version_base, 'component' : component}
        )

        with transaction.atomic():
            # We need to get the build number for this build as well as incrementing
            # the version's next_number field.  This all needs to be done atomically
            # as well so that 2 builds don't get the same build number.  Calling
            # select_for_update on the version will cause the model to get locked
            # so that no other requests can modify the model while we are within the
            # transaction.  
            version_base = VersionBase.objects.select_for_update().get(id=version_base.id)
            new_build_number = version_base.next_number
            version_base.next_number = new_build_number + 1
            version_base.save()

        build = Build(
            version_base=version_base, 
            branch=new_build.branch, 
            revision=new_build.revision,
            number=new_build_number
        )
        build.save()

        return build

class BuildHandler(APIView):
    """Handles API requests to get a single Build"""

    def get(self, request, pk, format=None):
        build = get_object_or_404(Build, pk=pk)
        serializer = BuildSerializer(build)
        return Response(serializer.data)

