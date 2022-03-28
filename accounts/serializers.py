from .models import User
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

class UserSerializer(RegisterSerializer):
    class Meta:
        model = User
        field = ('email','last_login','name', 'birthyear','community','create_date', 'updated_date','is_admin','is_active')