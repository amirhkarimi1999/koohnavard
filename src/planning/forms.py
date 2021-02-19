from django import forms

from .models import Plan, Charge, PlanPicture


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['title', 'description', 'destination_address', 'start_datetime', 'head_man', 'group_link']


class ChargeForm(forms.ModelForm):
    class Meta:
        model = Charge
        fields = ['title', 'description', 'amount']


class ReportForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['report']


class PlanPictureForm(forms.ModelForm):
    class Meta:
        model = PlanPicture
        fields = ['title', 'image', 'caption']
