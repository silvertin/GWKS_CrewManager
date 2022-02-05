from django.urls import path
from django.contrib.auth import views as auth_views
from common.views import UserCreateView, UserCreateDoneTV, UserLogout, UserLoginView

app_name = 'common'

urlpatterns = [
    path('login/', UserLoginView.as_view() , name='login'),
    path('logout/', UserLogout, name='logout'),

    path('register/', UserCreateView.as_view(), name='register'),
    path('register/done/', UserCreateDoneTV.as_view(), name='register_done'),
]