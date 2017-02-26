from rest_framework import serializers
from builds.models import Component, VersionBase, Build, NewBuild

class ComponentSerializer(serializers.ModelSerializer):
    """Serializer for the Application model"""
    versions = serializers.StringRelatedField(many=True)
    class Meta:
        model = Component
        fields = ('name', 'versions',)

class VersionBaseSerializer(serializers.ModelSerializer):
    """Serializer for the Version model"""
    builds = serializers.StringRelatedField(many=True)
    class Meta:
        model = VersionBase
        fields = ('value', 'builds')
    

class BuildSerializer(serializers.ModelSerializer):
    """Serializer for the Build model"""
    component = serializers.ReadOnlyField(source='component_name')
    version_base = serializers.SlugRelatedField(
        many=False, 
        read_only=True,
        slug_field='value'
    )
    class Meta:
        model = Build
        fields = ('component', 'version_base', 'branch', 'time', 'revision', 'number')
    
class NewBuildSerializer(serializers.ModelSerializer):
    """Serializer for the NewBuild model"""
    class Meta:
        model = NewBuild
        fields = ('component', 'version_base', 'branch', 'revision',)
