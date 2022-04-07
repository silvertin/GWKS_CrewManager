from django import forms
from CrewManager.models import Crew
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class CrewForm(forms.ModelForm):
    weekday = forms.MultipleChoiceField(choices=Crew.WeekDayType.choices, widget=forms.CheckboxSelectMultiple())
    community_limit = forms.MultipleChoiceField(choices=User.CommunityType.choices, widget=forms.CheckboxSelectMultiple())

    def clean_weekday(self):
        if len(self.cleaned_data['weekday']) > 1:
            raise forms.ValidationError('한개 요일만 선택하세요.')
        return self.cleaned_data['weekday']

    def save(self, commit=True):
        crew = super().save(commit=False)
        crew.weekday = self.cleaned_data['weekday'][0]
        crew.community_limit = self.cleaned_data['community_limit']
        if commit:
            crew.save()
        return crew

    class Meta:
        model = Crew
        fields = ['name','abstract', 'description', 'meeting_type','meeting_time', 'community', 'member_limit','meeting_limit','image']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'abstract' : forms.TextInput(attrs={'class':'form-control'}),
            'meeting_time' : forms.TextInput(attrs={'class' : 'form-control'}),
            'meeting_limit' : forms.TextInput(attrs={'class' : 'form-control'}),
            'member_limit' : forms.NumberInput()
        }