from django.shortcuts import get_object_or_404, render

# Create your views here.
# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from nameserver.models import Events
from rest_framework import status
from .serializers import EventsSerializer, EventSerializer
from rest_framework import mixins, viewsets

class EventsViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all().order_by('id')
    serializer_class = EventsSerializer


# The inputs to the following class apparently replace APIView
#class EventView(mixins.ListModelMixin, viewsets.GenericViewSet):
class EventView(APIView):

    def get(self, request):
        #events = Events.objects.all()
        #serializer = EventSerializer(events, many=True)
        return Response({"Error": "GET is not implemented for this service."})

    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

