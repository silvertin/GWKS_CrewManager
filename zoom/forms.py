from django import forms
from .models import ZoomAccount, ZoomMeeting, MEETING_TYPE_CHOICES, SETTINGS_SCHEMA
from django.core.validators import MinValueValidator, MaxValueValidator
from django_jsonform.widgets import JSONFormWidget



class ZoomMeetingForm(forms.ModelForm):
    class Meta:
        model = ZoomMeeting
        fields = ['topic', 'description', 'type_meeting','start_dt', 'duration', 'account','settings']
        widgets = {
            'topic' : forms.TextInput(attrs={'class':'form-control'}),
            'description' : forms.Textarea(attrs={'class':'form-control', 'rows':5}),
            'type_meeting' : forms.Select(attrs={'class':'form-control'},choices=MEETING_TYPE_CHOICES),
            'start_dt' : forms.DateTimeInput(attrs={'class':'form-control'}),
            'duration' : forms.NumberInput(attrs={'class':'form-control'}),
            'account' : forms.Select(attrs={'class':'form-control'}),
            'settings': JSONFormWidget(schema=SETTINGS_SCHEMA)
        }
