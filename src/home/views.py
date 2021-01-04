from django.contrib.auth.models import User
from django.shortcuts import render

from participation.models import Club
from planning.models import Plan


def home_page(request):
    """View function for home page of site."""

    user_cnt = User.objects.filter().count()
    club_cnt = Club.objects.filter().count()
    plan_cnt = Plan.objects.filter().count()

    context = {
        'user_cnt': user_cnt,
        'club_cnt': club_cnt,
        'plan_cnt': plan_cnt
    }

    # Render the HTML template home.html with the data in the context variable
    return render(request, 'home/home.html', context=context)
