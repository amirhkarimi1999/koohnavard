from django import forms

from .models import Plan, PlanParticipant, Charge
from markdownx.fields import MarkdownxFormField


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['title', 'description', 'destination_address', 'start_datetime', 'head_man', 'group_link']

class ChargeForm(forms.ModelForm):
    class Meta:
        model = Charge
        fields = ['title', 'description', 'amount']

class ReportForm(forms.Form):
    report = MarkdownxFormField()


