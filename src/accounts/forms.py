from django import forms
from django.contrib.auth.models import User

from accounts.models import UserProfile


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic']
