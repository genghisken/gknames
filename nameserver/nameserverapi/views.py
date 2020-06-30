from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import viewsets

from .serializers import EventsSerializer
from nameserver.models import Events


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all().order_by('id')
    serializer_class = EventsSerializer
