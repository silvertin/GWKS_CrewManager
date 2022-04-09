from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.views import ManagerOnlyMixin

from CrewManager.models import Crew
from CrewManager.forms import CrewForm

# Create your views here.
class CrewLV(ListView):
    model = Crew
    paginate_by = 10

class CrewDV(DetailView):
    model = Crew

class CrewCV(LoginRequiredMixin,CreateView):
    model = Crew
    form_class = CrewForm
    success_url = '/crew/'

    def form_valid(self, form):
        form.instance.manager = self.request.user
        form.instance.save()
        form.instance.members.add(self.request.user)

        return super().form_valid(form)

class CrewDelV(ManagerOnlyMixin,DeleteView):
    model = Crew
    success_url = '/crew/'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CrewUV(ManagerOnlyMixin,UpdateView):
    model = Crew
    form_class = CrewForm
    success_url = '/crew/'


def CrewJoin(request,pk):
    crew = get_object_or_404(Crew,pk=pk)
    if crew.members.count() >= crew.member_limit:
        return redirect('crew:detail', pk)
    else:
        if crew.members.filter(id=request.user.id).exists() and crew.manager.id != request.user.id:
            crew.members.remove(request.user)
        elif crew.manager.id == request.user.id:
            pass
        elif not str(request.user.id) in crew.community_limit:
            pass
        else:
            crew.members.add(request.user)
        return redirect('crew:detail', pk)


