from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _

from planning.models import Plan


class Club(models.Model):
    title = models.CharField(max_length=200,
                             blank=False,
                             null=False,
                             unique=True, verbose_name=_('title'))
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE, verbose_name=_('owner'))

    def __str__(self):
        return self.title


    @property
    def members_cnt(self):
        return ClubMember.objects.filter(club=self).filter(pending=False).count()


    @property
    def plans_cnt(self):
        return Plan.objects.filter(club=self).count()


class ClubMember(models.Model):
    club = models.ForeignKey(Club,
                             on_delete=models.CASCADE, verbose_name=_('club'))
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE, verbose_name=_('user'))

    pending = models.BooleanField(default=True, verbose_name=_('pending'))
