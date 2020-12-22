from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, verbose_name=_("profile_pic"))

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
