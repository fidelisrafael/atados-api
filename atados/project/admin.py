from django.contrib import admin
from atados.project.models import (Skill, Project,
                                   ProjectWork, ProjectDonation,
                                   Cause, Availability)


admin.site.register(Availability)
admin.site.register(Cause)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(ProjectWork)
admin.site.register(ProjectDonation)
