# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.db import connections
import urllib2
from atados_core.models import User
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils.encoding import iri_to_uri         

class Command(NoArgsCommand):
  help = "Get dates updated from legacy database."

  def handle_noargs(self, **options):

    print "Starting query for project created date..."
    cursor = connections['legacy_local'].cursor()
    cursor.execute(
      '''
       SELECT DISTINCT                                                                     
         node.uid,                                                                         
         image.filepath AS 'image'                                                      
       FROM                                                                                
         node                                                                              
       LEFT JOIN content_type_profile_ong ON content_type_profile_ong.nid = node.nid       
       LEFT JOIN files AS image ON image.fid = content_type_profile_ong.field_ong_foto_fid 
       WHERE node.type IN ('profile_ong')                                                  
      ;''')
                                                                                      
    desc = cursor.description
    print "Now processing....%d" % cursor.rowcount
    print
    i = 0                                                                               
    for row in cursor.fetchall():                                                       
      i = i + 1                                                                         
      row = dict(zip([col[0] for col in desc], row))                                    
      try:                                                                              
        user = User.objects.get(legacy_uid=row['uid'])                                  
        nonprofit = user.nonprofit                                                      
        imgurl = iri_to_uri("http://50.87.172.211/atados_antigo/site/%s" % row['image'])          
        image = NamedTemporaryFile(delete=True)                                      
        image.write(urllib2.urlopen(imgurl).read())                                  
        image.flush()                                                                
        left_path, extension = imgurl.rsplit('.', 1)                                 
        imgname = 'nonprofit/%s/%s.%s' % (user.slug, user.slug, extension)
        print imgname
        nonprofit.image.save(imgname, File(image))                                   
        print "%d - Nonprofit image saved... %s" % (i, nonprofit.name)               
                                                                                     
      except Exception as e:
        print e
