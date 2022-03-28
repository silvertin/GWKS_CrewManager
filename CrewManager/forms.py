from django import forms
from CrewManager.models import Crew
from django.core.validators import MinValueValidator, MaxValueValidator

class CrewForm(forms.ModelForm):

    class Meta:
        model = Crew
        fields = ['name', 'description', 'meeting_type','meeting_time', 'community', 'member_limit']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'meeting_time' : forms.TextInput(attrs={'class' : 'form-control'}),
            'member_limit' : forms.NumberInput()
        }