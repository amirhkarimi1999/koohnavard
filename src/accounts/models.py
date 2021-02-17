from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('first name'))
    last_name = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('last name'))
    email = models.EmailField(max_length=254, blank=True, null=True, verbose_name=_('email'))
    bio = models.CharField(max_length=400, blank=True, null=True, verbose_name=_('bio'))
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, verbose_name=_("profile_pic"))

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)