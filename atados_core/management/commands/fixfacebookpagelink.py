# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from atados_core.models import Nonprofit

import requests

class Command(BaseCommand):
  help = 'Fix URLs for nonprofits'

  def check_link(self, link):
    try:
      r = requests.get(link)
      if r.status_code == 404:
        print "404 " + link
    except:
      print "ERROR " + link
      if not "www" in link:
        link = "www." + link
      if not "http" in link:
        link = "https://" + link
    return link

  def handle(self, *args, **options):
    nonprofits = Nonprofit.objects.filter(published=True).order_by('id')
    for n in nonprofits:
      if n.facebook_page:
        new = self.check_link(n.facebook_page)
        if not n.facebook_page == new:
          print "NEW " + new
          n.facebook_page = new
          n.save()
      if n.website:
        new = self.check_link(n.website)
        if not n.website == new:
          print "NEW " + new
          n.website = new
          n.save()
