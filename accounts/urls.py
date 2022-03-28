from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.views import UserCreateView, UserCreateDoneTV, UserLogout, UserLoginView



app_name = 'accounts'

urlpatterns = [
    path('login/', UserLoginView.as_view() , name='login'),
    path('logout/', UserLogout, name='logout'),

    path('register/', UserCreateView.as_view(), name='register'),
    path('register/done/', UserCreateDoneTV.as_view(), name='register_done'),

    path('api/',include('dj_rest_auth.urls')),
    path('api/registration',include('dj_rest_auth.registration.urls')),
]