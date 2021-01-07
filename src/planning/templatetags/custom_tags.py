from django import template

register = template.Library()

from ..models import PlanNotification


@register.simple_tag(name='unseen_notifs')
def unseen_notifications_count(user):
    return PlanNotification.objects.filter(isSeen=2, user=user).count()
