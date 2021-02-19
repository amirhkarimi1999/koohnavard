import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _
from markdownx.models import MarkdownxField

# Create your models here.
from accounts.models import UserProfile


class Plan(models.Model):
    club = models.ForeignKey('participation.Club', null=False, on_delete=models.DO_NOTHING, verbose_name=_('club'))
    title = models.CharField(max_length=50, null=False, default="", verbose_name=_('title'))
    description = models.CharField(max_length=256, null=False, default="", verbose_name=_('description'))
    destination_address = models.CharField(max_length=256, null=False, default="",
                                           verbose_name=_('destination_address'))
    start_datetime = models.DateTimeField(verbose_name=_('start_datetime'), default=datetime.date.today)
    head_man = models.CharField(max_length=256, null=False, default="", verbose_name=_('head_man'))
    group_link = models.URLField(default="", verbose_name=_('group_link'))
    report = MarkdownxField(default='')

    def __str__(self):
        return str(self.title) + " " + str(self.club)

    @property
    def head_man_user(self):
        return User.objects.get(username=self.head_man)


    @property
    def participants_cnt(self):
        return PlanParticipant.objects.filter(plan=self).filter(
            status=str(PlanParticipant.MemberStatus.ACCEPTED)).count()


class Charge(models.Model):
    plan = models.ForeignKey('planning.Plan', null=False, on_delete=models.DO_NOTHING, verbose_name=_('club'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    title = models.CharField(max_length=50, null=False, default="", verbose_name=_('title'))
    description = models.CharField(max_length=256, null=False, default="", verbose_name=_('description'))
    amount = models.DecimalField(max_digits=20, decimal_places=0, null=False, verbose_name=_('amount'))


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
    role = models.CharField(max_length=40, null=True, verbose_name=_('role'))

    @property
    def getUser(self):
        return UserProfile.objects.get(user=self.user)

    @property
    def user_total_pay(self):
        charges = Charge.objects.filter(plan=self.plan, user=self.user)
        totalPlanCarges = 0
        for p in charges:
            totalPlanCarges += p.amount
        return totalPlanCarges

class PlanNotification(models.Model):
    plan = models.ForeignKey(Plan, null=False, on_delete=models.CASCADE, verbose_name=_('plan'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    title = models.CharField(max_length=50, null=False, default="", verbose_name=_('title'))
    description = models.CharField(max_length=256, null=False, default="", verbose_name=_('description'))
    time = models.DateTimeField(verbose_name=_('time'))
    isSeen = models.IntegerField(default=2, verbose_name=_('isSeen'))


class PlanPicture(models.Model):
    plan = models.ForeignKey('planning.Plan', null=False, on_delete=models.DO_NOTHING, verbose_name=_('club'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    title = models.CharField(max_length=50, null=False, default="", verbose_name=_('title'))
    caption = models.CharField(max_length=256, null=False, default="", verbose_name=_('caption'))
    image = models.ImageField(null=False, verbose_name=_('image'), upload_to='plan_pictures')
    isPublic = models.BooleanField(default=False, verbose_name=_('isPublic'))
