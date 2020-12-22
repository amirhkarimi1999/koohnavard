from django import forms

from .models import Plan, PlanParticipant


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['title', 'description', 'destination_address', 'start_datetime', 'head_man', 'group_link']



