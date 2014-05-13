# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from atados_core.models import Nonprofit

import requests

class Command(BaseCommand):
  help = 'Fix URLs for nonprofits Facebook Page'

  def check_link(self, link):
    try:
      r = requests.get(link)
      if r.status_code == 200:
        print "OK " + link

      elif r.status_code == 404:
        print "404 " + link
    except:
      print "ERROR"

  def handle(self, *args, **options):
    nonprofits = Nonprofit.objects.all()
    linksFixed = 0
    for n in nonprofits:
      if n.facebook_page:
        try:
          self.check_link(n.facebook_page)
        except:
          if not "www" in n.facebook_page:
            n.facebook_page = "www." + n.facebook_page
          n.facebook_page = "http://" + n.facebook_page
          n.save()
          self.check_link(n.facebook_page)

        linksFixed = linksFixed + 1

    self.stdout.write('Fixed %s' % linksFixed)
