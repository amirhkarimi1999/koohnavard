from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest

from accounts.models import UserProfile
from planning.models import PlanParticipant
from .models import Club, ClubMember
from .forms import ClubForm


def clubs_list_view(request):
    if request.user.is_authenticated:
        my_reqs = ClubMember.objects.filter(user=request.user, pending=False)
        my_clubs = list(map(lambda req: req.club, my_reqs))

        pending_reqs = ClubMember.objects.filter(user=request.user, pending=True)
        pending_clubs = list(map(lambda req: req.club, pending_reqs))


        other_clubs = list(filter(lambda club: club not in my_clubs and club not in pending_clubs, Club.objects.all()))
        return render(request,
                'participation/clubs_list.html',
                {
                    'auth': True,
                    'my_clubs': my_clubs,
                    'pending_clubs': pending_clubs,
                    'other_clubs': other_clubs,
                })
    else:
        return render(request,
                'participation/clubs_list.html',
                {
                    'auth': False,
                    'clubs': Club.objects.all(),
                })


def club_profile_view(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    members = club.clubmember_set.filter(pending=False)
    owner = get_object_or_404(UserProfile, user=club.owner)
    req = ClubMember.objects.filter(user=request.user, club=club).first()
    return render(request,
            'participation/club_profile.html',
            {
                'club': club,
                'owner': owner,
                'members': members,
                'is_mine': club.owner == request.user,
                'is_member': req is not None and not req.pending,
                'is_pending': req is not None and req.pending,
            })


@login_required
def edit_club_view(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    if club.owner != request.user:
        return HttpResponseForbidden()
    form = ClubForm(request.POST or None, instance=club)
    if request.method == 'POST':
        if form.is_valid():
            club = form.save()
            return HttpResponseRedirect(reverse('participation:club_view',
                args=(club.id,)))
    return render(request,
            'participation/club_edit.html',
            {
                'form': form,
                'club': club,
            })


@login_required
def club_requests_view(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    is_owner = club.owner == request.user
    reqs = ClubMember.objects.filter(club=club, pending=True)
    temp = []
    for m in reqs:
        temp.append(get_object_or_404(UserProfile, user=m.user))
    reqs = temp
    members = ClubMember.objects.filter(club=club, pending=False)
    temp = []
    for m in members:
        temp.append(get_object_or_404(UserProfile, user=m.user))
    members = temp
    return render(request,
            'participation/club_requests.html',
            {
                'reqs': reqs if is_owner else [],
                'members': members,
                'club': club,
                'is_owner': is_owner,
            })


@login_required
def create_club_view(request):
    form = ClubForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            club = form.save(commit=False)
            club.owner = request.user
            club.save()
            ClubMember.objects.create(user=club.owner, club=club, pending=False)
            return HttpResponseRedirect(reverse('participation:club_view',
                args=(club.id,)))
    return render(request,
            'participation/club_create.html',
            {'form': form})


@login_required
def join_request_view(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    member = ClubMember.objects.filter(club=club, user=request.user)
    if member.count() != 0 or member.first() == club.owner:
        return HttpResponseBadRequest()
    ClubMember.objects.create(user=request.user, club=club)
    return HttpResponseRedirect(reverse('participation:clubs_list'))


@login_required
def leave_request_view(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    member = ClubMember.objects.filter(club=club, user=request.user)
    if member.count() == 0 or member.first() == club.owner:
        return HttpResponseBadRequest()
    member.delete()
    return HttpResponseRedirect(reverse('participation:clubs_list'))


@login_required
def answer_request_view(request, req_id, accept):
    req = get_object_or_404(ClubMember, pk=req_id)
    club = req.club
    if club.owner != request.user:
        return HttpResponseForbidden()
    if accept:
        req.pending = False
        req.save()
    elif req.user != club.owner:
        req.delete()
    return HttpResponseRedirect(reverse('participation:club_join_requests', args=(club.id,)))


@login_required
def kick_club_member_view(request, req_id):
    return answer_request_view(request, req_id, 0)

