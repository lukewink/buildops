import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "verstore.settings")

import django
django.setup()

from builds.models import Application, Version, Build
from builds.serializers import ApplicationSerializer, VersionSerializer, BuildSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


b = Build.objects.all()[0]
serializer = BuildSerializer(b)
content = JSONRenderer().render(serializer.data)
print(content)
