from django.urls import path
from .views import ZoomAccountLV, ZoomMeetingLV, getajaxlist, \
    ZoomMeetingDV, ZoomMeetingCV, ZoomMeetingDelV, ZoomMeetingUV

app_name = 'zoom'


urlpatterns = [
    path('account/',ZoomAccountLV.as_view(), name='accountlist'),

    path('meeting/',ZoomMeetingLV.as_view(), name='meetinglist'),
    path('meeting/getlist', getajaxlist, name='meetinglistupdate'),
    path('meeting/<int:pk>', ZoomMeetingDV.as_view(), name='meetingdetail'),
    path('meeting/new', ZoomMeetingCV.as_view(), name='meetingnew'),
    path('meeting/<int:pk>/delete', ZoomMeetingDelV.as_view(), name='meetingdelete'),
    path('meeting/<int:pk>/update', ZoomMeetingUV.as_view(), name='meetingupdate'),

]