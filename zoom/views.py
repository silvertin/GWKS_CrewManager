import datetime
import pytz

from django.utils import timezone
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .models import ZoomAccount, ZoomMeeting
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

import json
from .forms import ZoomMeetingForm
from .zoom import Zoom

# Create your views here.
class ZoomAccountDV(LoginRequiredMixin,DetailView):
    model = ZoomAccount
    template_name = 'zoom/zoomaccount_detail.html'


class ZoomAccountLV(LoginRequiredMixin,ListView):
    model = ZoomAccount
    template_name = 'zoom/zoomaccount_list.html'

class ZoomMeetingDV(DetailView):
    model = ZoomMeeting
    template_name = 'zoom/zoommeeting_detail.html'

class ZoomMeetingDelV(LoginRequiredMixin,DeleteView):
    model = ZoomMeeting
    template_name = 'zoom/zoommeeting_confirm_delete.html'
    success_url = '/zoom/meeting/'

class ZoomMeetingUV(LoginRequiredMixin,UpdateView):
    model = ZoomMeeting
    form_class = ZoomMeetingForm
    success_url = '/zoom/meeting/'

class ZoomMeetingCV(LoginRequiredMixin,CreateView):
    model = ZoomMeeting
    form_class = ZoomMeetingForm
    success_url = '/zoom/meeting/'

    def form_valid(self, form):
        self.object = form.save(commit=False)

        #여기에 추가로 저장할것 작성
        #self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class ZoomMeetingLV(ListView):
    model = ZoomMeeting
    template_name = 'zoom/zoommeeting_list.html'

    def get(self, request, *args, **kwargs):
        za = ZoomAccount.objects.filter(available=True)
        update_db(za)
        return super().get(request,*args,**kwargs)

def create_meeting(ZoomAccount, date, topic, duration, password):
    if ZoomAccount.available:
        zw = Zoom(ZoomAccount.appkey, ZoomAccount.secretkey, ZoomAccount.useremail)
        zw.CreateMeeting()


def update_db(ZoomAccount):
    for za in ZoomAccount:
        zm = ZoomMeeting.objects.filter(account=za)
        zw = Zoom(za.appkey, za.secretkey, za.useremail)
        zoom_list = zw.getlist()['meetings']
        for zl in zoom_list:
            if zm.filter(meetingid=zl['id']).exists():
                if zl['type'] == 8:
                    if not zm.filter(start_dt=zl['start_time']).exists():
                        data = ZoomMeeting(
                            meetingid=zl['id'],
                            topic=zl['topic'],
                            description='없음(줌 계정에서 생성)',
                            type_meeting=zl['type'],
                            create_dt=zl['created_at'],
                            duration=zl['duration'],
                            password='None',
                            join_url=zl['join_url'],
                            account=za
                        )
                        data.start_dt = zl['start_time']
                        data.save()
                    else:
                        pass
                else:
                    pass
            else:
                data = ZoomMeeting(
                    meetingid= zl['id'],
                    topic=zl['topic'],
                    description='없음(줌 계정에서 생성)',
                    type_meeting=zl['type'],
                    create_dt=zl['created_at'],
                    duration=zl['duration'],
                    password='None',
                    join_url=zl['join_url'],
                    account=za
                )
                if data.type_meeting != 3:
                    data.start_dt = zl['start_time']
                data.save()


def getajaxlist(request):
    KST = pytz.timezone('Asia/Seoul')
    datestr = list(request.GET.dict().keys())[0][:10]
    date_start = datetime.datetime.strptime(datestr,'%Y-%m-%d')
    zm = ZoomMeeting.objects.filter(start_dt__date = date_start.date())
    return_data = list()
    for d in zm:
        dict_data = {
            'id': d.meetingid,
            'name': d.topic,
            'start': d.start_dt.astimezone(KST).strftime("%Y-%m-%d %H:%M"),
            'end': (d.start_dt.astimezone(KST) + datetime.timedelta(minutes=d.duration)).strftime("%Y-%m-%d %H:%M"),
            'pk': d.id
        }
        return_data.append(dict_data)
    jsonObject = json.dumps(return_data)
    return HttpResponse(jsonObject,content_type="application/json")