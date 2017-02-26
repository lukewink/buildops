from rest_framework import serializers
from builds.models import Application, Version, Build, NewBuild

class ApplicationSerializer(serializers.ModelSerializer):
    """Serializer for the Application model"""
    versions = serializers.StringRelatedField(many=True)
    class Meta:
        model = Application
        fields = ('name', 'versions',)

class VersionSerializer(serializers.ModelSerializer):
    """Serializer for the Version model"""
    builds = serializers.StringRelatedField(many=True)
    class Meta:
        model = Version
        fields = ('version', 'builds')
    

class BuildSerializer(serializers.ModelSerializer):
    """Serializer for the Build model"""
    application = serializers.ReadOnlyField(source='application_name')
    version = serializers.SlugRelatedField(
        many=False, 
        read_only=True,
        slug_field='version'
    )
    class Meta:
        model = Build
        fields = ('application', 'version', 'branch', 'time', 'revision', 'number')
    
class NewBuildSerializer(serializers.ModelSerializer):
    """Serializer for the NewBuild model"""
    class Meta:
        model = NewBuild
        fields = ('application', 'version', 'branch', 'revision',)
