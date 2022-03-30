from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import crew_list, crew_detail, user_list, user_detail

app_name = 'apis'

urlpatterns = [
    path('crew/', crew_list),
    path('crew/<int:pk>/', crew_detail),
    path('user/', user_list),
    path('user/<int:pk>/', user_detail),

]