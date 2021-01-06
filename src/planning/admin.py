from django.contrib import admin

# Register your models here.
from planning.models import Plan, PlanParticipant, PlanNotification, PlanPicture

admin.site.register(Plan)
admin.site.register(PlanParticipant)
admin.site.register(PlanNotification)
admin.site.register(PlanPicture)
