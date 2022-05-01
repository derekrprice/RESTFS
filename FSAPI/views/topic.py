from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from FSAPI.models import Topic


class TopicView(APIView):
    """
        PUT replaces a Topic.
    """
    @csrf_exempt
    def delete(self, request, pk):
        deleted = Topic.objects.filter(pk=pk).delete()

        if deleted[0] == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response({"deleted": deleted}, status=status.HTTP_200_OK)
