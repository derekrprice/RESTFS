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

    @csrf_exempt
    def get(self, request, path=''):

        try:
            folder = Folder.objects.get(name='/%s' % path)
        except Folder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        parent = os.path.dirname('/%s' % path)

        try:
            if len(path) == 0:
                escaped_path = ''
            else:
                escaped_path = '/' + ''.join('\\u%04x' % ord(c) for c in path)
            subfolders = Folder.objects.filter(name__regex=r'^%s/[^/]+$' % escaped_path).all()
            documents = Document.objects.filter(name__regex=r'^%s/[^/]+$' % escaped_path).all()
        except Folder.DoesNotExist:
            subfolders = []

        data = {
            "name": folder.name,
            "topics": [topic.name for topic in folder.topics.all()],
            "up": request.build_absolute_uri('/folders' + parent),
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

        try:
            existing = Folder.objects.get(name='/%s' % path)
        except Folder.DoesNotExist:
            existing = None

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
