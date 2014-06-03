# -*- coding: utf-8 -*- 

from django.contrib import admin
from atados_core.models import Nonprofit, Project, User, Address, Role, Work, Job, City
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin.util import lookup_field
from django.utils.html import strip_tags
from django.contrib import messages
from pyExcelerator import Workbook
from atados import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html

class NonprofitAdmin(admin.ModelAdmin):
  fields = ['id', 'name', 'url', 'description',
            ('published', 'deleted'),
            'details', 'image', 'image_tag', 'cover', 'cover_tag', 'website', 'facebook_page', 'google_page', 'twitter_handle', 'causes']
  list_display = ['id', 'name', 'description', 'published', 'deleted', 'created_date', 'get_address']
  list_filter = ('published', 'deleted')
  search_fields = ['name']
  actions = ['make_published']
  readonly_fields = ['id', 'url', 'image_tag', 'cover_tag']

  def url(self, instance):
   return format_html("<a href='https://www.atados.com.br/ong/{0}' target='_blank'>Clique para ver ong no site</a>", instance.user.slug)

  def make_published(self, request, queryset):
      queryset.update(published=True)
  make_published.short_description = _("Mark selected Nonprofits as published")

class UserInline(admin.TabularInline):
    model = User
class ProjectInline(admin.TabularInline):
    model = Project
class WorkInline(admin.TabularInline):
    model = Work
class JobInline(admin.TabularInline):
    model = Job

class AddressAdmin(admin.ModelAdmin):
  readonly_fields = ['id']
  fields = ('city', 'addressline', 'addressline2', 'addressnumber', 'neighborhood', 'zipcode', ('latitude', 'longitude'))
  raw_id_fields = ['city']
  related_lookup_fields = {
      'city': ['city'],
  }
  list_display = ('id', 'object', 'addressline', 'addressnumber', 'neighborhood', 'city', 'zipcode', 'latitude', 'longitude')
  search_fields = ['id']

  def object(self, instance):
    try:
      project = instance.project
      return "%s" % ("(Ato) ", project)
    except:
      try:
        user = instance.user
        try:
            user.nonprofit
            return u"(ONG) %s" % user
        except:
            return u"(Voluntário) %s" % user
      except:
        company = instance.company
        return "%s" % ("(Empresa) ", company)

class CityAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'state', 'active')
  search_fields = ['name', 'id']
  list_filter = ['active']

class RoleAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'prerequisites', 'details', 'vacancies')
  search_fields = ['name', 'id']

class ProjectAdmin(admin.ModelAdmin):
  fields = ('id', 'url', 'work', 'job', ('name', 'slug'),
        'nonprofit', 'description', 'details', 'address_id', 'highlighted', 'image', 'image_tag',
        'responsible', 'phone', 'email',
        ('published', 'closed', 'deleted'),
        'roles', 'skills', 'causes')
  list_display = ('id', 'name', 'slug', 'nonprofit', 'description', 'published', 'closed', 'deleted', 'created_date', 'city', 'address_id', 'work', 'job')
  list_filter = ['published', 'deleted', 'closed']
  list_editable = ['published', 'closed']
  search_fields = ['name', 'slug']
  readonly_fields = ['id', 'url', 'image_tag', 'work', 'job', 'address_id']
  filter_horizontal = ('roles',)

  def city(self, instance):
      return instance.address.get_city_state() if instance.address else None

  def address_id(self, instance):
      return instance.address.id if instance.address else None

  def url(self, instance):
   return format_html("<a href='https://www.atados.com.br/ato/{0}' target='_blank'>Clique para ver ato no site</a>", instance.slug)

class JobAdmin(admin.ModelAdmin):
  list_display = ('id', 'project', 'start_date', 'end_date')

class WorkAdmin(admin.ModelAdmin):
  list_display = ('id', 'project', 'weekly_hours', 'can_be_done_remotely')
  search_fields = ('id', )
  filter_horizontal = ('availabilities',)

class UserAdmin(admin.ModelAdmin):
  fields = ('name', 'slug', 'email', 'phone')
  list_display = ('slug', 'email', 'name', 'last_login')
  list_filter = ('last_login', 'joined_date')
  search_fields = ('email', 'slug')

admin.site.register(Nonprofit, NonprofitAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(City, CityAdmin)



def export_as_xls(modeladmin, request, queryset):
    """
    Generic xls export admin action.
    """
    if queryset.count() > settings.EXPORT_RECORDS_LIMIT:
        messages.error(request, "Can't export more then %s Records in one go. Narrow down your criteria using filters or search" % str(settings.EXPORT_RECORDS_LIMIT))
        return HttpResponseRedirect(request.path_info)
    fields = []

    #PUT THE LIST OF FIELD NAMES YOU DON'T WANT TO EXPORT
    exclude_fields = [] 

    #foreign key related fields
    extras = ['']

    if not request.user.is_staff:
        raise PermissionDenied

    for f in modeladmin.list_display:
        if f not in exclude_fields:
            fields.append(f)
    fields.extend(extras)
    
    opts = modeladmin.model._meta

    wb = Workbook()
    ws0 = wb.add_sheet('0')
    col = 0
    field_names = []

    # write header row
    for field in fields:
        ws0.write(0, col, field)
        field_names.append(field)
        col = col + 1
    row = 1

    # Write data rows
    for obj in queryset:
        col = 0
        for field in field_names:
            if field in extras:
                try:
                    val = [eval('obj.'+field)] #eval sucks but easiest way to deal
                except :
                    val = ['None']
            else:
                try:
                    val = lookup_field(field, obj, modeladmin)
                except :
                    val = ['None']

            if not val[-1] == None:
              if isinstance(val[-1], bool):
                ws0.write(row, col, strip_tags(str(val[-1])))
              elif not isinstance(val[-1], str) and not isinstance(val[-1], unicode):
                ws0.write(row, col, strip_tags(val[-1].__unicode__()))
              elif val[-1]:
                ws0.write(row, col, strip_tags(val[-1]))
            else:
              ws0.write(row, col, strip_tags(''))


            col = col + 1
        
        row = row + 1

    wb.save('/tmp/output.xls')
    response = HttpResponse(open('/tmp/output.xls','r').read(),
                  mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s.xls' % unicode(opts).replace('.', '_')
    return response

export_as_xls.short_description = _("Export selected to XLS")
admin.site.add_action(export_as_xls)
