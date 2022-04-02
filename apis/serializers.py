from rest_framework.serializers import ModelSerializer
from CrewManager.models import Crew
from accounts.models import User

class CrewSerializer(ModelSerializer):
    class Meta:
        model = Crew
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        ref_name = "User 1"