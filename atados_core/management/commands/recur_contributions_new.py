# -*- coding: utf-8 -*-
import os
import requests
import json

from django.core.management.base import NoArgsCommand
from atados_core.models import User, Subscription
from dateutil.relativedelta import relativedelta
from datetime import datetime

class Command(NoArgsCommand):
  help = "Recur contributions(new system)"

  def handle_noargs(self, **options):
    """ This method is the one executed when the command is ran.
        It should select all initial contributions, generate a payment table
        from the date the payment was made up to now, check which payments
        were made and request the pending payments.
    """

    print "Recurring contributions(new)"
    subs = Subscription.objects.filter(recurrent=True, parent=None, active=True, status="paid")

    for sub in subs:
      children = Subscription.objects.filter(parent=sub).order_by('-created_date')
      sub_month = self.get_sub_month(sub)
      payment_dict = self.fill_payment_dict(self.generate_payment_dict(sub), children)

      print "---------"
      print "[{}] {} - {} - {}".format(sub.id, sub.name.encode('utf8'), sub.status, sub_month)
      print "Payment dict:", payment_dict

      self.request_payments(payment_dict, sub)

      print "---------"
      #print ":: Ending after first ::"
      #break

  def get_sub_month(self, sub):
    """ Returns a string like 10/2015 """
    return sub.created_date.strftime('%m/%Y')

  def generate_payment_dict(self, sub):
    """ Returns a dict where the keys correspond to the payment month, and the value refers to the Subscription id.
        Eg. {'10/2015': 1, '11/2015': None, '12/2015': None, '01/2016': None}
        The last key is, as expected, the current month if the payment day has passed
        or last month if it's not payment day yet
    """
    payment_dict = {}
    start_day    = sub.created_date.day
    start_month  = sub.created_date.month
    start_year   = sub.created_date.year

    now = datetime.now()
    end_day   = now.day
    end_month = now.month
    end_year  = now.year

    for year in range(start_year, end_year+1):
      for month in range(1, 12+1):
        if ( (year == start_year and month >= start_month) or
             (year == end_year and month < end_month) or
             (year == end_year and month == end_month and start_day <= end_day) or
             (year not in [start_year, end_year]) ):
          payment_dict['{}/{}'.format(month, year)] = None

    payment_dict[self.get_sub_month(sub)] = sub.id

    return payment_dict

  def fill_payment_dict(self, payment_dict, children):
    """ This method takes an payment_dict and fill the respective months
        with the Subscription id
    """
    for child in children:
      pass
    return payment_dict

  def request_payments(self, payment_dict, sub):
    """ Check all the months, if any of them doesn't have a payment id then request payment """
    for date, payment_id in payment_dict.iteritems():
      if not payment_id:
        print "Payment for {} not found, requesting...".format(date)
        self.process_payment(sub, date)

  def process_payment(self, sub, date):
    """ Create payment at pagar.me and save to database """
    print "lol"
