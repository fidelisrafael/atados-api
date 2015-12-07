# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from atados_core.models import User, Subscription
from dateutil.relativedelta import relativedelta
from datetime import datetime

class Command(NoArgsCommand):
  help = "Recur contributions"

  def handle_noargs(self, **options):
    print "Recurring contributions"
    subs = Subscription.objects.filter(recurrent=True, parent=None, active=True)
    for sub in subs:
      children = Subscription.objects.filter(parent=sub).order_by('-created_date')
      compare_date = sub.created_date

      if children.count():
        compare_date = children[0].created_date

      compare_date = (compare_date + relativedelta(months=+1)).replace(tzinfo=None)
      if compare_date < datetime.now():
        print "{}: {}".format(sub.name, compare_date)
