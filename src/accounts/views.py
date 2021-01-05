from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.views import generic

from planning.models import PlanParticipant, PlanNotification

from accounts.forms import UserRegisterForm, UserProfileInfoForm
from accounts.models import UserProfile


def index(request):
    return HttpResponseRedirect(reverse('participation:clubs_list'))


def register(request):
    # TODO permissions and roles not implemented
    """ redirecting to home if authenticated """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('participation:clubs_list'))
    """ registering """
    if request.method == 'POST':
        user_form = UserRegisterForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            login(request, user)
            return HttpResponseRedirect(reverse('participation:clubs_list'))
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserRegisterForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'accounts/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


def login_user(request):
    """ redirecting to home if authenticated """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('participation:clubs_list'))
    """ logging in """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('accounts:index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'accounts/login.html', {})


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('participation:clubs_list'))


@login_required
def duties(request):
    planParticipants = PlanParticipant.objects.filter(user=request.user,
                                                      status=str(PlanParticipant.MemberStatus.ACCEPTED),
                                                      duty__isnull=False)
    return render(request, 'accounts/duties.html', {'planParticipants': planParticipants})


@login_required
def profile_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:register'))
    profile_form = UserProfileInfoForm(data=request.POST or None)
    if request.method == 'POST':
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            user = get_object_or_404(UserProfile, user=request.user)
            if 'profile_pic' in request.FILES:
                print('found profile pic')
                user.profile_pic = request.FILES['profile_pic']
            if profile.first_name :
                user.first_name = profile.first_name
            if profile.last_name :
                user.last_name = profile.last_name
            if profile.email :
                user.email = profile.email
            if profile.bio:
                user.bio = profile.bio
            user.save()
            return HttpResponseRedirect(reverse('accounts:seeProfile'))
        else:
            print(profile_form.errors)
    return render(request, 'accounts/profile.html', {'profile_form': profile_form})

@login_required
def see_profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:register'))
    else:
        user = get_object_or_404(UserProfile, user=request.user)
        return render(request, 'accounts/see_profile.html', {'userProfile': user})

# class UserEditView(generic.UpdateView):
#     form_class = UserProfileInfoForm
#     template_name = 'accounts/profile.html'
#     success_url = reverse_lazy('participation:clubs_list')
#
#     def get_object(self, queryset=None):
#         return self.request.user

@login_required
def seeInbox(request):
    notifications = PlanNotification.objects.filter(user=request.user).order_by('-time')
    for notif in notifications:
        notif.isSeen = max(0, notif.isSeen - 1)
        notif.save()
    return render(request, 'accounts/inbox.html', {'notifications': notifications})
