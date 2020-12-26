from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.views import generic

from planning.models import PlanParticipant

from accounts.forms import UserRegisterForm, UserProfileInfoForm


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
    for pp in planParticipants:
        if not pp.isDutySeen:
            pp.isDutySeen = True
            pp.save()
    return render(request, 'accounts/duties.html', {'planParticipants': planParticipants})


@login_required
def profile_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:register'))
    profile_form = UserProfileInfoForm(data=request.POST or None)
    if request.method == 'POST':
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            if 'profile_pic' in request.FILES:
                print('found profile pic')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            return HttpResponseRedirect(reverse('participation:clubs_list'))
        else:
            print(profile_form.errors)
    return render(request, 'accounts/profile.html', {'profile_form': profile_form})


# class UserEditView(generic.UpdateView):
#     form_class = UserProfileInfoForm
#     template_name = 'accounts/profile.html'
#     success_url = reverse_lazy('participation:clubs_list')
#
#     def get_object(self, queryset=None):
#         return self.request.user
