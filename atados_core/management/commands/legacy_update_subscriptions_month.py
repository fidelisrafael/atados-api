# -*- coding: utf-8 -*-
import os
import requests
import json

from django.core.management.base import NoArgsCommand
from atados_core.models import User, Subscription
from dateutil.relativedelta import relativedelta
from datetime import datetime

class Command(NoArgsCommand):
  help = "Update subscriptions month to use new recurring system(single-time use only)"

  def handle_noargs(self, **options):
    print "Updating contributions month(legacy)"
    subs = Subscription.objects.filter()
    for sub in subs:
      sub.month = self.get_sub_month(sub)
      sub.save()

  def get_sub_month(self, sub):
    """ Returns a string like 10/2015 """
    return sub.created_date.strftime('%m/%Y')
