from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DocumentSerializer, FolderSerializer
from .models import Document, Folder

import os.path


class FolderView(APIView):

    def get(self, request, path=''):
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
            "subfolders": [request.build_absolute_uri('/folders' + subfolder.name) for subfolder in subfolders],
            "documents": [DocumentSerializer(document).data for document in documents],
        }
        return Response(data)

    def put(self, request, path=''):
        # Parent folder must exist.
        try:
            Folder.objects.get(name=os.path.dirname('/%s' % path))
        except Folder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        existing = Folder.objects.get(name='/%s' % path)

        if existing and 'content' in request.data:
            return Response({"status": "error", "data": {"content":["Target is a folder."]}}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

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
