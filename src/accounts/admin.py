from django.contrib import admin

# Register your models here.
from accounts.models import UserProfile
from planning.models import PlanNotification

admin.site.register(UserProfile)


