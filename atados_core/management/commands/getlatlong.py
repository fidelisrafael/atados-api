# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from atados_core.models import Project, Address

from pygeocoder import Geocoder

class Command(BaseCommand):
  help = 'Read address from csv and get latitude and longitude from google'

  def handle(self, *args, **options):
    ids = Project.objects.values_list('address_id', flat=True)
    for a in Address.objects.filter(id__in=ids):
      if a.latitude == 0 or a.longitude == 0:
        if a.addressline:
          try:                                         
            print a
            results = Geocoder.geocode(a)
            a.latitude = results[0].coordinates[0]
            a.longitude = results[0].coordinates[1]
            print "%s %s" %(a.latitude, a.longitude)
          except Exception as e:                       
            print e                                    

      #raise CommandError('Poll "%s" does not exist' % poll_id)
    #self.stdout.write('Successfully closed poll "%s"' % poll_id)
