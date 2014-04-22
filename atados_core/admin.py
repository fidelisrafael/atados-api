from django.contrib import admin
from atados_core.models import Nonprofit, Project, User, Address
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin.util import lookup_field
from django.utils.html import strip_tags
from django.contrib import messages
from pyExcelerator import Workbook
from atados import settings
from django.utils.translation import ugettext_lazy as _

class NonprofitAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'description', 'published', 'deleted', 'get_address', 'created_date')
  list_filter = ('published', 'deleted')
  search_fields = ['name']
  actions = ['make_published']

  def make_published(self, request, queryset):
      queryset.update(published=True)
  make_published.short_description = _("Mark selected stories as published")

class AddressAdmin(admin.ModelAdmin):
  list_display = ('id', 'city', 'latitude', 'longitude', 'addressline')
  search_fields = ['id']

class ProjectAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'slug', 'nonprofit', 'description', 'published', 'closed', 'deleted', 'address', 'created_date')
  list_filter = ('published', 'deleted', 'closed')
  search_fields = ['name', 'slug', 'nonprofit']
  raw_id_fields = ['address']
  related_lookup_fields = {
    'address': ['address']
  }

class UserAdmin(admin.ModelAdmin):
  list_display = ('slug', 'email', 'name', 'last_login')
  list_filter = ('last_login', 'joined_date')
  search_fields = ('email', 'slug')

admin.site.register(Nonprofit, NonprofitAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(User, UserAdmin)



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
