from django.contrib import admin

# Register your models here.
from planning.models import Plan, PlanParticipant

admin.site.register(Plan)
admin.site.register(PlanParticipant)
