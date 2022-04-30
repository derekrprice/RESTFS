from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DocumentSerializer, FolderSerializer
from .models import Document, Folder


class FolderView(APIView):

    @csrf_exempt
    def get(self, request, path=''):

        try:
            for name in path.split('/'):
                folder = Folder.objects.get(parent=1, name=name)
        except Folder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = {
            "id": folder.id,
            "name": folder.name,
            "topics": [f"%s" % topic for topic in folder.topics.all()],
        }
        return Response(data)
