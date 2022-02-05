from django.urls import path
from .views import CrewLV, CrewDV, CrewCV, CrewDelV, CrewUV, CrewJoin
from django.contrib.auth.decorators import login_required

app_name = 'crew'

urlpatterns = [
    path('', CrewLV.as_view(), name='list'),
    path('<int:pk>/', CrewDV.as_view(), name='detail'),
    path('new/', login_required(CrewCV.as_view()), name='new'),
    path('<int:pk>/delete/', login_required(CrewDelV.as_view()), name='delete'),
    path('<int:pk>/update/', login_required(CrewUV.as_view()), name='update'),
    path('<int:pk>/join/', login_required(CrewJoin), name='join')
]