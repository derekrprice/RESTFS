from rest_framework import serializers
from .models import Document, Folder


class DocumentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    topics = serializers.StringRelatedField(many=True, read_only=True)
    content = serializers.CharField(max_length=4096)

    class Meta:
        model = Document
        fields = ('__all__',)


class FolderIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = ('id',)


class FolderSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    topics = serializers.StringRelatedField(many=True, read_only=True)
    document = DocumentSerializer(many=True)
    folder = FolderIdSerializer(many=True)

    class Meta:
        model = Folder
        fields = ('id', 'name', 'topics', 'document', 'folder')

    # def to_representation(self, instance):
