from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.views.generic import CreateView

from django.contrib.auth import login, logout, authenticate
#from django.contrib.auth.forms import UserCreationForm
from accounts.forms import CrewUserCreationForm, CrewUserLoginForm
from django.contrib.auth.mixins import AccessMixin

from django.http import HttpResponseRedirect, HttpResponse

from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.
class ManagerOnlyMixin(AccessMixin):
    raise_exception = True
    permission_denied_message = "크루매니저만 수정/삭제가 가능합니다."

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.manager:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(FormView):
    form_class = CrewUserLoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        credentials = form.cleaned_data

        user = authenticate(username=credentials['email'],
                            password=credentials['password'])

        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)
        else:
            messages.add_message(self.request, messages.INFO, '등록된 정보가 없습니다. 다시 시도해주세요')
            return HttpResponseRedirect(reverse_lazy('accounts:login'))


def UserLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))

class UserCreateView(CreateView):
    template_name = 'accounts/register.html'
    form_class= CrewUserCreationForm
    success_url = reverse_lazy('accounts:register_done')

class UserCreateDoneTV(TemplateView):
    template_name = 'accounts/register_done.html'