# -*- coding: utf-8 -*-

from __future__ import absolute_import

from celery.decorators import task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from atados_core.models import Project, User, Address, City

@task
def send_email_to_volunteer_after_4_weeks_of_apply(volunteer_email, project_id):
    try:
      project = Project.objects.get(id=project_id)
    except Exception as e:
      print e
      return

    # 4 semanas após voluntário se candidatar a um ato
    plaintext = get_template('email/volunteerAfterApply4Weeks.txt')
    htmly     = get_template('email/volunteerAfterApply4Weeks.html')
    d = Context({ "project_name": project.name })
    subject, from_email, to = u'Como anda o voluntariado?', 'Associação Atados <site@atados.com.br>', volunteer_email
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@task
def send_email_to_volunteer_3_days_before_pontual(volunteer_email, project_id):
    try:
      project = Project.objects.get(id=project_id)
    except Exception as e:
      print e
      return

    plaintext = get_template('email/volunteer3DaysBeforePontual.txt')
    htmly     = get_template('email/volunteer3DaysBeforePontual.html')
    d = Context({ "project_name": project.name })
    subject, from_email, to = u'Um ato está chegando... estamos ansiosos para te ver.', 'Associação Atados <site@atados.com.br>', volunteer_email
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@task
def send_email_to_donator_after_7_days_of_subscription(donator_email):
    plaintext = get_template('email/successfulDonation3DaysAfter.txt')
    htmly     = get_template('email/successfulDonation3DaysAfter.html')
    d = Context({})
    subject, from_email, to = u'Veja só os descontos que ganhou com sua doação!', 'Associação Atados <site@atados.com.br>', donator_email
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@task
def add_volunteer_address_from_csv():
  import csv
  with open('users.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
      try:
        id = int(row[0])
        u = User.objects.get(pk=row[0])

        if (u.address and not u.address.city) or not u.address:
          print row[4]
          address = Address()
          address.city = City.objects.get(id=row[4])
          address.save()
          u.address = address
          u.save()
      except:
        pass
