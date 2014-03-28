# -*- coding: utf-8 -*-
import sys
import pytz
from datetime import datetime
from django.core.management.base import NoArgsCommand
from django.db import connections
from atados_core.models import Project, User, Apply, ApplyStatus

class Command(NoArgsCommand):
  help = "Get apply created updated from legacy database."

  def handle_noargs(self, **options):

    cursor = connections['legacy'].cursor()
    cursor.execute(
      '''
        SELECT DISTINCT                                                                
           flag_content.uid AS 'uid',      
           flag_content.content_id AS 'nid',
           flag_content.timestamp AS 'date'                                             
         FROM                                                                           
           flag_content                                                                 
         LEFT JOIN users ON flag_content.uid = users.uid                                
         WHERE flag_content.fid = 4
      ;''')
                                                                                      
    desc = cursor.description
    print "Now processing....%d" % cursor.rowcount
    print
    i = 0
    new = 0
    for row in cursor.fetchall():
      i = i + 1
      row = dict(zip([col[0] for col in desc], row))
      try:
        volunteer = User.objects.get(legacy_uid=row['uid']).volunteer
        project = Project.objects.get(legacy_nid=row['nid'])
        try:
          apply = Apply.objects.get(volunteer=volunteer, project=project)
        except:
          apply = Apply()                                                                                        
          apply.volunteer = volunteer                                                                            
          apply.project = project                                                                                
          apply.date = datetime.utcfromtimestamp(row['date']).replace(tzinfo=pytz.timezone("America/Sao_Paulo"))
          apply.status = ApplyStatus.objects.get(name="Candidato")                                              
          print "%s %s" % (apply.volunteer, apply.project)
          new = new + 1
          apply.save()                                                                                           
      except Exception as e: 
        print "ERROR - %d - %s" % (sys.exc_traceback.tb_lineno, e)
    print new
