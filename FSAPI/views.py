from django.shortcuts import render

# Create your views here.
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DocumentSerializer, FolderSerializer, TopicSerializer
from .models import Document, Folder, Topic

import os.path


class FolderView(APIView):
    """
        GET     returns a list of all the Folders and Documents contained within a Folder with an optional `topics=` filter
                which filters topics by name.

        PUT     manages Folders and Documents.

        DELETE  would delete a Folder or Document, recursively deleting children, but I have left
                it disabled for purposes of this demo.
    """
    @csrf_exempt
    def get(self, request, path=''):
        # Folder must exist.
        try:
            folder = Folder.objects.get(name='/%s' % path)
        except Folder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        parent_name = os.path.dirname('/%s' % path)
        topics = request.query_params['topics'].split(',') if 'topics' in request.query_params else None
        escaped_path = '' if len(path) == 0 else '/' + ''.join('\\u%04x' % ord(c) for c in path)

        subfolders_query = Folder.objects.filter(name__regex=r'^%s/[^/]+$' % escaped_path)
        subfolders = subfolders_query.filter(topics__name__in=topics).all() if topics else subfolders_query.all()

        documents_query = Document.objects.filter(name__regex=r'^%s/[^/]+$' % escaped_path)
        documents = documents_query.filter(topics__name__in=topics).all() if topics else documents_query.all()

        data = {
            "name": folder.name,
            "topics": [topic.name for topic in folder.topics.all()],
            "up": request.build_absolute_uri('/folders' + parent_name),
            "folders": [request.build_absolute_uri('/folders' + subfolder.name) for subfolder in subfolders],
            "documents": [DocumentSerializer(document).data for document in documents],
            "query": request.query_params if request.query_params else {},
        }
        return Response(data)

    @csrf_exempt
    def put(self, request, path=''):
        # Parent folder must exist.
        try:
            Folder.objects.get(name=os.path.dirname('/%s' % path))
        except Folder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            existing = Folder.objects.get(name='/%s' % path)
        except Folder.DoesNotExist:
            existing = None

        if existing and 'content' in request.data:
            return Response({"status": "error", "data": {"content":["Target is a folder."]}}, status=status.HTTP_409_CONFLICT)

        data = {**request.data, "name": '/%s' % path}
        if 'content' in request.data:
            serializer = DocumentSerializer(existing, data=data)
        else:
            serializer = FolderSerializer(existing, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @csrf_exempt
    def delete(self, request, path=''):
        if path in ['', '/']:
            return Response(status=status.HTTP_403_FORBIDDEN)

        escaped_path = '/' + ''.join('\\u%04x' % ord(c) for c in path)
        deleted = Folder.objects.filter(name__regex=r'^%s(/|$)' % escaped_path).delete()
        return Response({"count": deleted}, status=status.HTTP_200_OK)


class TopicListView(APIView):
    """
        GET Returns a list of all the Topics, with an optional fuzzy `contains=` filter
        that is matched against either name or description.
    """
    @csrf_exempt
    def get(self, request):
        contains = request.query_params['contains'] if 'contains' in request.query_params else ''
        rx = '.*'.join('\\u%04x' % ord(c) for c in contains)
        topics = Topic.objects.filter(Q(name__regex=rx) | Q(description__regex=rx)).all() if rx else Topic.objects.all()

        data = {
            "count": topics.count(),
            "data": [TopicSerializer(topic).data for topic in topics],
            "query": request.query_params if request.query_params else {},
        }
        return Response(data)


class TopicView(APIView):
    """
        PUT replaces a Topic.
    """
    @csrf_exempt
    def put(self, request, pk):
        try:
            existing = Topic.objects.get(pk=pk)
        except Topic.DoesNotExist:
            existing = None

        serializer = TopicSerializer(existing, request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
