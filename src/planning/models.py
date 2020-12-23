from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class Plan(models.Model):
    club = models.ForeignKey('participation.Club', null=False, on_delete=models.DO_NOTHING, verbose_name=_('club'))
    title = models.CharField(max_length=50, null=False, default="", verbose_name=_('title'))
    description = models.CharField(max_length=256, null=False, default="", verbose_name=_('description'))
    destination_address = models.CharField(max_length=256, null=False, default="",
                                           verbose_name=_('destination_address'))
    start_datetime = models.DateTimeField(verbose_name=_('start_datetime'))
    head_man = models.CharField(max_length=256, null=False, default="", verbose_name=_('head_man'))
    group_link = models.URLField(default="", verbose_name=_('group_link'))

    def __str__(self):
        return str(self.title) + " " + str(self.club)

    @property
    def head_man_user(self):
        return User.objects.get(username=self.head_man)


    @property
    def participants_cnt(self):
        return PlanParticipant.objects.filter(plan=self).filter(
            status=str(PlanParticipant.MemberStatus.ACCEPTED)).count()


class PlanParticipant(models.Model):
    class MemberStatus(models.TextChoices):
        PENDING = "PENDING",
        ACCEPTED = "ACCEPTED",
        REJECTED = "REJECTED",

        @classmethod
        def choices(cls):
            print(tuple((i.name, i.value) for i in cls))
            return tuple((i.name, i.value) for i in cls)

    plan = models.ForeignKey(Plan, null=False, on_delete=models.CASCADE, verbose_name=_('plan'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    status = models.CharField(max_length=255, choices=MemberStatus.choices, verbose_name=_('status'))
    duty = models.CharField(max_length=1000, null=True, verbose_name=_('duty'))
