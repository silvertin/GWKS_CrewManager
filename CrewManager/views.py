import datetime
from io import BytesIO

import pandas as pd
from django.http import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from accounts.views import ManagerOnlyMixin

from CrewManager.models import Crew
from CrewManager.forms import CrewForm

from accounts.models import User

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
        u = User.objects.get(id=request.user.id)
        if crew.members.filter(id=request.user.id).exists() and crew.manager.id != request.user.id:
            crew.members.remove(request.user)
        elif crew.manager.id == request.user.id:
            pass
        elif not str(u.community) in crew.community_limit:
            pass
        else:
            crew.members.add(request.user)
        return redirect('crew:detail', pk)

@staff_member_required
def crewlist_excel_export(request):
    user = User.objects.all()

    data = []

    for u in user:
        d = {}
        d['이름'] = u.name
        d['소속'] = User.CommunityType.choices[u.community]
        d['이메일'] = u.email
        d['참여크루'] = [c.name for c in Crew.objects.filter(members__in=[u])]
        data.append(d)

    output = BytesIO()

    df = pd.DataFrame(data, columns=['이름', '소속', '이메일','참여크루'])

    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()

    output.seek(0)
    # workbook = output.getvalue()
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    response = StreamingHttpResponse(output,
                                     content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=user_data_{date}.xlsx'
    return response
