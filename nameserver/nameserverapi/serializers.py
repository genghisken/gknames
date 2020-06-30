# serializers.py
from rest_framework import serializers

from nameserver.models import Events

class EventsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Events
        fields = ('id', 'ra', 'decl', 'ra_original', 'decl_original', 'date_inserted', 'date_updated', 'year', 'base26suffix', 'htm16id')
