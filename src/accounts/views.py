from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

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
def profile(request):
    return render(request, 'accounts/profile.html')



