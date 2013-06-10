from django.contrib import admin
from atados_nonprofit.models import Nonprofit

class NonprofitAdmin(admin.ModelAdmin):
    list_filter = ('published',)
    exclude = ('deleted', 'deleted_date',)

    def queryset(self, request):
        qs = self.model._default_manager.active()
        ordering = self.ordering or () 
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

admin.site.register(Nonprofit, NonprofitAdmin)
