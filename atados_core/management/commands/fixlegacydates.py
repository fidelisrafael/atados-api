# -*- coding: utf-8 -*-
import sys
import pytz
from datetime import datetime
from django.core.management.base import NoArgsCommand
from django.db import connections
from atados_core.models import Project, User, Apply

class Command(NoArgsCommand):
  help = "Get dates updated from legacy database."

  def handle_noargs(self, **options):

    print "Starting query for project created date..."
    cursor = connections['legacy'].cursor()
#    cursor.execute(
#        '''
#          SELECT DISTINCT                                                                              
#             node.nid,                                                                                   
#             node.uid,                                                                                                                                                    
#             node.created AS 'created',
#             node.changed AS 'modified' 
#           FROM                                                                                          
#             node                                                                                              
#           WHERE node.type IN ('ato_recorrente', 'ato_doacao', 'ato_pontual')                            
#           GROUP BY node.nid                                                                             
#           ORDER BY node.uid
#          ;''')
#
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
    print "Now processing....%d nonprofits" % cursor.rowcount
    print
    i = 0
    for row in cursor.fetchall():
      i = i + 1
      row = dict(zip([col[0] for col in desc], row))
      try:
        project = Project.objects.get(legacy_nid=row['nid'])
        user = User.objects.get(legacy_uid=row['uid'])
        volunteer = user.volunteer
        date = datetime.utcfromtimestamp(row['date']).replace(tzinfo=pytz.timezone("America/Sao_Paulo"))
        a = Apply.objects.get(volunteer=volunteer, project=project)
        if a.date != date:
          a.date = date
          print a.date
          a.save()
        #print "%s %s" % (project.name, user.name)
#        project = Project.objects.get(legacy_nid=row['nid'])
#
#        created_date = datetime.utcfromtimestamp(row['created']).replace(tzinfo=pytz.timezone("America/Sao_Paulo"))
#        if project.created_date != created_date:
#          project.created_date = created_date
#          print project.created_date
#          project.save()
#
#        print "Project modified date..."
#        modified_date = datetime.utcfromtimestamp(row['modified']).replace(tzinfo=pytz.timezone("America/Sao_Paulo"))
#        if project.modified_date != modified_date:
#          project.modified_date = modified_date
#          print project.modified_date
#          project.save()
#          print project.modified_date

      except Exception as e: 
        print "ERROR - %d - %s" % (sys.exc_traceback.tb_lineno, e)
