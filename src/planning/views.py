from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext as _

from participation.models import Club, ClubMember
from .forms import PlanForm
from .models import Plan, PlanParticipant


def plans_list_view(request, club_id=0):
    clubs = []
    if club_id > 0:
        clubs = Club.objects.filter(pk=club_id)
    elif club_id == 0:
        clubs = Club.objects.all()
    elif club_id == -1 and request.user.is_authenticated:
        memberships = ClubMember.objects.filter(user=request.user).filter(pending=False)
        clubs = map(lambda memb: memb.club, memberships)

    plans = []
    for club in clubs:
        plans += list(club.plan_set.all())
    my_plans = None
    if request.user.is_authenticated:
        my_plans = PlanParticipant.objects.filter(user=request.user, status=str(PlanParticipant.MemberStatus.ACCEPTED))
        my_plans = map(lambda memb: memb.plan, my_plans)
        my_plans = filter(lambda plan: plan in plans, my_plans)
        my_plans = list(my_plans)
        my_plans.sort(key=lambda plan: plan.start_datetime)
        my_plans.reverse()

    return render(request, 'planning/plans_list.html', {
        'plans': plans,
        'my_plans': my_plans,
    })


def plan_profile_view(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id)
    plan_participant = None
    if request.user.is_authenticated and PlanParticipant.objects.filter(user=request.user, plan=plan).count():
        plan_participant = PlanParticipant.objects.get(user=request.user, plan=plan)
    return render(request,
                  'planning/plan_profile.html',
                  {'plan': plan,
                   'plan_participant': plan_participant})


@login_required
def edit_plan_view(request, plan_id):
    # TODO permissions and roles not implemented
    plan = get_object_or_404(Plan, pk=plan_id)
    plan_head_man_list = User.objects.filter(username=plan.head_man)
    if plan.club.owner != request.user and (len(plan_head_man_list) == 0 or plan_head_man_list.first() != request.user):
        return HttpResponseForbidden()
    form = PlanForm(request.POST or None, instance=plan)
    if request.method == 'POST':
        if form.is_valid():
            """ creating plan """
        """ adding head man to plan participant """

        plan = form.save(commit=False)
        if User.objects.filter(username=plan.head_man).count() != 0 and ClubMember.objects.filter(
                user=plan.head_man_user, pending=False, club=plan.club).count() != 0:
            plan.save()
            if PlanParticipant.objects.filter(user=plan.head_man_user, plan=plan).count() == 0:
                parti = PlanParticipant()
                parti.user = plan.head_man_user
                parti.plan = plan
                parti.MemberStatus = str(PlanParticipant.MemberStatus.ACCEPTED)
                parti.save()

            return HttpResponseRedirect(reverse('planning:plan_view',
                                                args=[plan.id]))
        else:
            form.add_error('head_man', _("Invalid head man username"))
            return render(request,
                          'planning/plan_edit.html', {
                              'form': form,
                              'plan': plan,
                          })
    return render(request,
                  'planning/plan_edit.html',
                  {'form': form, 'plan': plan})


@login_required
def create_plan_view(request, club_id):
    # TODO permissions and roles not implemented
    club = get_object_or_404(Club, pk=club_id)
    if request.user != club.owner:
        return HttpResponseForbidden()
    form = PlanForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            """ creating plan """
            """ adding head man to plan participant """

            plan = form.save(commit=False)
            parti = PlanParticipant()
            if User.objects.filter(username=plan.head_man).count() != 0 and ClubMember.objects.filter(
                    user=plan.head_man_user, pending=False, club=club).count() != 0:
                parti.user = plan.head_man_user

                plan.club = club

                parti.plan = plan
                parti.MemberStatus = str(PlanParticipant.MemberStatus.ACCEPTED)

                plan.save()
                parti.save()

                return HttpResponseRedirect(reverse('planning:plan_view',
                                                    args=[plan.id]))
            else:
                form.add_error('head_man', _("Invalid head man username"))
                return render(request,
                              'planning/plan_create.html', {
                                  'form': form,
                                  'club_id': club_id,
                              })

    return render(request,
                  'planning/plan_create.html', {
                      'form': form,
                      'club_id': club_id,
                  })


@login_required
def plan_participant_preregister(request, plan_id):
    # TODO permissions and roles not implemented - Check for user club registration
    plan = get_object_or_404(Plan, pk=plan_id)
    if PlanParticipant.objects.filter(user=request.user).filter(plan=plan).count():
        return HttpResponseBadRequest("you are already a part of this plan!")
    PlanParticipant.objects.create(user=request.user, status=str(PlanParticipant.MemberStatus.PENDING), plan=plan)
    return HttpResponseRedirect(reverse('planning:plan_view',
                                        args=[plan.id]))


@login_required
def plan_members_and_requests_view(request, plan_id):
    ## TODO for requests
    plan = get_object_or_404(Plan, pk=plan_id)
    members = PlanParticipant.objects.filter(plan=plan, status=str(PlanParticipant.MemberStatus.ACCEPTED))
    pending = PlanParticipant.objects.filter(plan=plan, status=str(PlanParticipant.MemberStatus.PENDING))
    if not ClubMember.objects.filter(club=plan.club, user=request.user).count():
        return HttpResponseForbidden()
    edit_access = False
    if plan.head_man_user == request.user or plan.club.owner == request.user:
        edit_access = True
    return render(request,
                  'planning/plan_members_and_requests.html',
                  {
                      'members': members,
                      'pending': pending if edit_access else [],
                      'plan': plan,
                      'edit_access': edit_access
                  })


@login_required
def answer_request_view(request, req_id, accept):
    req = get_object_or_404(PlanParticipant, pk=req_id)
    plan = req.plan
    if plan.head_man != str(request.user) and plan.club.owner != request.user:
        return HttpResponseForbidden()
    if accept == 'ACCEPT':
        req.status = PlanParticipant.MemberStatus.ACCEPTED
    elif accept == 'REJECT':
        req.status = PlanParticipant.MemberStatus.REJECTED
    req.save()
    return HttpResponseRedirect(reverse('planning:plan_join_members_and_requests', args=(plan.id,)))
