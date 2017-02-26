from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from builds.models import Application, Version, Build, NewBuild
from builds.serializers import ApplicationSerializer, VersionSerializer, BuildSerializer, NewBuildSerializer

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'builds': reverse('build-list', request=request, format=format),
    })

class BuildsHandler(APIView):
    """Handles API requests to get and create builds."""

    def get(self, request, format=None):
        """Get all the builds in the database"""
        builds = Build.objects.all()
        serializer = BuildSerializer(builds, many = True)
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
            return Response(build_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create_build(self, new_build):
        """Create a new Build model from a NewBuild instance"""

        # Get/Create the Application model that is associated with this new build.
        # Note that the query is case insensitive on the name.  This way 'VxStorage'
        # and 'vxstorage' will refer to the same Application.
        app, _ = Application.objects.get_or_create(
            name__iexact=new_build.application,
            defaults={'name' : new_build.application}
        )
        
        # Get/Create the Version model that is associated with the new build.
        version, _ = Version.objects.get_or_create(
            version__iexact=new_build.version,
            defaults={'version' : new_build.version, 'application' : app}
        )

        with transaction.atomic():
            # We need to get the build number for this build as well as incrementing
            # the version's next_number field.  This all needs to be done atomically
            # as well so that 2 builds don't get the same build number.  Calling
            # select_for_update on the version will cause the model to get locked
            # so that no other requests can modify the model while we are within the
            # transaction.  
            version = Version.objects.select_for_update().get(id=version.id)
            new_build_number = version.next_number
            version.next_number = new_build_number + 1
            version.save()

        build = Build(
            version=version, 
            branch=new_build.branch, 
            revision=new_build.revision,
            number=new_build_number
        )
        build.save()
        return build