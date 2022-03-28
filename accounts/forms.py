from django import forms
from accounts.admin import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import User


class CrewUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        models = get_user_model()
        fields = ['email','name','password1','password2','birthyear', 'community']
        widgets = {
            'email' : forms.EmailInput(attrs={'class':'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'birthyear': forms.NumberInput(attrs={'class': 'form-control'}),
            'community': forms.Select(attrs={'class': 'form-control'})
        }


class CrewUserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())



class SignupForm(forms.Form):
    email = forms.EmailField(label='이메일', widget=forms.TextInput(attrs={'class':'form-control'}))
    name = forms.CharField(label='이름', widget=forms.TextInput(attrs={'class':'form-control'}))
    birthyear = forms.IntegerField(label='또래', widget=forms.NumberInput(attrs={'class':'form-control'}))
    community = forms.ChoiceField(label='소속 공동체', choices=User.CommunityType.choices, widget=forms.Select(attrs={'class':'form-control'}))

    def signup(self, request, user):
        user.name = self.cleaned_data['name']
        user.birthyear = self.cleaned_data['birthyear']
        user.community = self.cleaned_data['community']
        user.save()
        return user