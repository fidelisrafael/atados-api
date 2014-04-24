# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from atados_core.models import Nonprofit, Project


class Command(BaseCommand):
  args = '<old_slug new_slug>'
  help = 'Change slug name for for nonprofit'

  def handle(self, *args, **options):
    try:
      old_slug, new_slug = args
    except:
      raise CommandError('Need to input both old and new slug')

    try:
      nonprofit = Nonprofit.objects.get(user__slug=old_slug)
    except:
      raise CommandError('There is no nonprofit with this slug: %s' % old_slug)

    nonprofit.user.slug = new_slug

    try:
        top_level, image = nonprofit.image.name.rsplit('/', 1)
        name, extension = nonprofit.image.name.rsplit('.', 1)
        nonprofit.image.name = "%s/%s.%s" % (top_level, new_slug, extension)
    except:
        pass

    try:
        top_level, image = nonprofit.cover.name.rsplit('/', 1)
        name, extension = nonprofit.cover.name.rsplit('.', 1)
        nonprofit.cover.name = "%s/%s.%s" % (top_level, new_slug, extension)
    except:
        pass

    projects = Project.objects.filter(nonprofit=nonprofit)
    for p in projects:
        try:
            top_level, image = p.image.name.rsplit('/', 1)
            project_folder, slug = top_level.rsplit('/', 1)
            p.image.name = "%s/%s/%s" % (project_folder, new_slug, image)
            p.save()
        except:
            pass
    nonprofit.save()
    nonprofit.user.save()
    self.stdout.write('Successfully changed from %s to %s ' % (old_slug, new_slug))
