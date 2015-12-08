# -*- coding: utf-8 -*-
import os
import requests
import json

from django.core.management.base import NoArgsCommand
from atados_core.models import User, Subscription
from dateutil.relativedelta import relativedelta
from datetime import datetime

class Command(NoArgsCommand):
  help = "Recur contributions"

  def handle_noargs(self, **options):
    print "Recurring contributions"
    subs = Subscription.objects.filter(recurrent=True, parent=None, active=True, status="paid")
    for sub in subs:
      children = Subscription.objects.filter(parent=sub).order_by('-created_date')
      compare_date = sub.created_date

      if children.count():
        compare_date = children[0].created_date

      compare_date = (compare_date + relativedelta(months=+1)).replace(tzinfo=None)
      if compare_date < datetime.now():
          print "[{}][{}] {}: - Expected: {}".format(sub.id, children.count(), sub.name, compare_date)

          # Duplicating sub
          new_sub = sub
          new_sub.parent_id = sub.id
          new_sub.pk = None
          new_sub.recurrent = False
          new_sub.created_date = datetime.now()
          new_sub.status = None
          new_sub.status_reason = None
          new_sub.tid = None
          new_sub.save()

          # Prepare data
          data = {'amount': int(sub.value*100), 'card_id': sub.card_id, 'api_key': os.environ.get('ATADOS_API_KEY')}

          # Dump data log
          with open("pag.txt", "a") as f:
            f.write("[R] Data: {}\n".format(json.dumps(data)))

          # Request pagar.me
          r = requests.post('https://api.pagar.me/1/transactions', params=data)
          resp = json.loads(r.text)

          # Dump response log
          with open("pag.txt", "a") as f:
            f.write("[R] Response: {}\n".format(r.text.encode('utf8')))

          new_sub.tid = resp.get('tid', None)
          new_sub.status = resp.get('status', None)
          new_sub.status_reason = resp.get('status_reason', None)
          new_sub.save()
