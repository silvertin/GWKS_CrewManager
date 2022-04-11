from django import forms
from CrewManager.models import Crew
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class CrewForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CrewForm,self).__init__(*args,**kwargs)
        if Crew.objects.filter(id=self.instance.id).exists():
            c = Crew.objects.filter(id=self.instance.id).get()
            self.fields['weekday'].initial = c.weekday
            self.fields['community_limit'].initial = c.community_limit

    weekday = forms.MultipleChoiceField(label="크루 모임 요일 (가능한 요일 하루만 선택해주세요)",choices=Crew.WeekDayType.choices, widget=forms.CheckboxSelectMultiple())
    community_limit = forms.MultipleChoiceField(label="크루 가입 가능 공동체 (가입가능공동체 모두 선택해주세요)",choices=User.CommunityType.choices, widget=forms.CheckboxSelectMultiple())

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
        fields = \
            ['name','abstract', 'description', 'meeting_type',
             'community', 'member_limit','meeting_limit','image',
             'period', 'start_time','end_time','meeting_time', 'kakao_room'
             ]
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'abstract' : forms.TextInput(attrs={'class':'form-control'}),
            'meeting_time' : forms.TextInput(attrs={'class' : 'form-control'}),
            'meeting_limit' : forms.TextInput(attrs={'class' : 'form-control'}),
            'member_limit' : forms.NumberInput(),
            'start_time' : forms.TimeInput(attrs={'class':'form-control'}),
            'end_time' : forms.TimeInput(attrs={'class':'form-control'}),
            'kakao_room' : forms.URLInput(attrs={'class':'form-control'})
        }