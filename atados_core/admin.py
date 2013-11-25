from django.contrib import admin
from atados_core import models

class ProjectAdmin(admin.ModelAdmin):
    list_filter = ('published',)
    exclude = ('deleted', 'deleted_date',)

    def queryset(self, request):
        qs = self.model._default_manager.active()
        ordering = self.ordering or () 
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

class NonprofitAdmin(admin.ModelAdmin):
    list_filter = ('published',)
    exclude = ('deleted', 'deleted_date',)

    def queryset(self, request):
        qs = self.model._default_manager.active()
        ordering = self.ordering or () 
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

admin.site.register(models.Nonprofit)
admin.site.register(models.Apply)
admin.site.register(models.Availability)
admin.site.register(models.Cause)
admin.site.register(models.Skill)
admin.site.register(models.Project)
admin.site.register(models.Donation)
admin.site.register(models.Work)
admin.site.register(models.Job)
admin.site.register(models.Role)
admin.site.register(models.Recommendation)
admin.site.register(models.State)
admin.site.register(models.City)
admin.site.register(models.Suburb)
admin.site.register(models.Address)
admin.site.register(models.Volunteer)
