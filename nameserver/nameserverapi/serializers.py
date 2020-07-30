# serializers.py
from rest_framework import serializers
from nameserver.models import *
from nameserver.views import years
from gkhtm._gkhtm import htmID
from gkutils.commonutils import coneSearchHTM, FULL, CAT_ID_RA_DEC_COLS, base26, Struct
from datetime import datetime
from django.db import connection
from django.db import IntegrityError

RADIUS = 3.0 # arcsec
MULTIPLIER = 10000000

# I can't believe that this works! The events table is not part of my long list,
# but we can add it here.
CAT_ID_RA_DEC_COLS['events'] = [['id', 'ra', 'decl'],1017]


# Return all the events
class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ('id', 'ra', 'decl', 'ra_original', 'decl_original', 'date_inserted', 'date_updated', 'year', 'base26suffix')
        #fields = '__all__'


# Receive and add a new event
# Counter is optional - it should only be provided as part of the ingest
# process for existing data.
class EventSerializer(serializers.Serializer):
    internalObjectId = serializers.IntegerField(required=True)
    internalName = serializers.CharField(max_length=20)
    ra = serializers.FloatField(required=True)
    decl = serializers.FloatField(required=True)
    flagDate = serializers.DateField(required=False, default=datetime.now())
    counter = serializers.IntegerField(required=False, default=0)
    survey_database = serializers.CharField(required=True, max_length=20)


    def save(self):

        from django.conf import settings
        ra = self.validated_data['ra']
        decl = self.validated_data['decl']
        internalObjectId = self.validated_data['internalObjectId']
        internalName = self.validated_data['internalName']
        survey_database = self.validated_data['survey_database']

        # Get the authenticated user, if it exists.
        userId = 'unknown'
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            userId = str(request.user)

        print ("EXTRACTED USER ID = ", userId)
        htm16id = htmID(16, ra, decl)

        flagDate = self.validated_data['flagDate']
        #if not flagDate:
        #    flagDate = datetime.now()

        year = flagDate.year

        acquiredId = 0

        counter = self.validated_data['counter']
        if counter is not None and counter > 0:
            acquiredId = (year - 2000) * MULTIPLIER + counter

        if not flagDate:
            flagDate = datetime.now()

        replyMessage = 'Object created'

        # Is there an object within RADIUS arcsec of this object?
        message, results = coneSearchHTM(ra, decl, RADIUS, 'events', queryType = FULL, conn = connection, django = True)

        # So - if there are NO matches, insert into the relevant year based
        # on either the flag date OR choose from the current year.
        # But if there ARE matches, shove into the AKAs table with the RA and
        # dec.  We may use this later to recalculate the RA and Dec in the
        # events table.
        if len(results) > 0:
            event = Struct(**results[0][1])
            separation = results[0][0]
            replyMessage = 'Object already exists'

            try:
                aka = Akas(ra = ra,
                           decl = decl,
                           event_id_id = event.id,
                           object_id = internalObjectId,
                           aka = internalName,
                           survey_database = survey_database,
                           user_id = userId,
                           source_ip = None,
                           htm16id = htm16id)
                aka.save()
            except IntegrityError as e:
                #print(e[0])
                #if e[0] == 1062: # Duplicate Key error
                replyMessage = 'Duplicate AKA - cannot add AKA'

        else:
            if acquiredId != 0:
                y = years[year](id = acquiredId,
                                ra = ra,
                                decl = decl,
                                object_id = internalObjectId,
                                survey_database = survey_database,
                                user_id = userId,
                                source_ip = None,
                                htm16id = htm16id)
            else:
                y = years[year](ra = ra,
                                decl = decl,
                                object_id = internalObjectId,
                                survey_database = survey_database,
                                user_id = userId,
                                source_ip = None,
                                htm16id = htm16id)
            y.save()

            acquiredId = y.pk
            suffix = base26(acquiredId - (MULTIPLIER * (year - 2000)))
            event = Events(id = acquiredId,
                           ra = ra,
                           decl = decl,
                           ra_original = ra,
                           decl_original = decl,
                           year = year,
                           base26suffix = suffix,
                           htm16id = htm16id)

            event.save()

            # Add the aka
            try:
                aka = Akas(ra = ra,
                           decl = decl,
                           event_id_id = acquiredId,
                           object_id = internalObjectId,
                           aka = internalName,
                           survey_database = survey_database,
                           user_id = userId,
                           source_ip = None,
                           htm16id = htm16id)
                aka.save()
            except IntegrityError as e:
                #print(e[0])
                #if e[0] == 1062: # Duplicate Key error
                replyMessage = 'Duplicate AKA - cannot add new AKA'

        objectName = settings.OBJECT_PREFIX + "%d" % (year - 2000) + event.base26suffix
        #return event

        info = { "event_id": objectName, "info": replyMessage }
        return info

