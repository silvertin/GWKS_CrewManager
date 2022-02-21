from django.urls import path
from zoom import views


app_name = 'zoom'

urlpatterns = [
    path('',views.index, name='index')
]