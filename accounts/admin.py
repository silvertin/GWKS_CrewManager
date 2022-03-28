from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from accounts.models import User

# Register your models here.
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="비밀번호", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="비밀번호 확인", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email', 'name', 'birthyear', 'community')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("비밀번호가 동일하지 않습니다.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'is_active', 'is_admin', 'birthyear', 'community')

class UserAdmin(BaseUserAdmin):
   # The forms to add and change user instances
   form = UserChangeForm
   add_form = UserCreationForm

   # The fields to be used in displaying the User model.
   # These override the definitions on the base UserAdmin
   # that reference specific fields on auth.User.
   list_display = ('email', 'name', 'is_admin', 'birthyear','community')
   list_filter = ('is_admin',)
   fieldsets = (
       (None, {'fields': ('email', 'password')}),
       ('Personal info', {'fields': ('name', 'birthyear','community')}),
       ('Permissions', {'fields': ('is_admin',)}),
   )
   # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
   # overrides get_fieldsets to use this attribute when creating a user.
   add_fieldsets = (
       (None, {
           'classes': ('wide',),
           'fields': ('email', 'name', 'password1', 'password2', 'birthyear', 'community'),
       }),
   )
   search_fields = ('email',)
   ordering = ('email',)
   filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)