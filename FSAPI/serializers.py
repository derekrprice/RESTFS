from rest_framework import serializers
from .models import Document, Folder, Topic


class DocumentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    topics = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Topic.objects.all())
    content = serializers.CharField(max_length=4096)

    class Meta:
        model = Document
        fields = ('name', 'topics', 'content')
        lookup_field = 'name'


class FolderSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    topics = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Topic.objects.all())

    class Meta:
        model = Folder
        fields = ('name', 'topics')
        lookup_field = 'name'
