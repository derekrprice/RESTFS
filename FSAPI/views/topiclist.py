from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from FSAPI.models import Topic
from FSAPI.serializers import TopicSerializer


class TopicListView(APIView):
    """
        GET returns a list of all the Topics, with an optional fuzzy `contains=` filter
        that is matched against either name or description.

        POST creates a new topic.
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

    @csrf_exempt
    def post(self, request):
        serializer = TopicSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        try:
            existing = Topic.objects.get(name=serializer.validated_data['name'])
        except Topic.DoesNotExist:
            existing = None

        if existing:
            # No dup names.
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer.save()
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
