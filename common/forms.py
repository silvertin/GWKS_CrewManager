from django import forms
from common.admin import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

class CrewUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        models = get_user_model()
        fields = ['email','name','password1','password2']


class CrewUserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())