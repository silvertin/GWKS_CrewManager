from rest_framework.serializers import ModelSerializer, ImageField
from CrewManager.models import Crew
from accounts.models import User

class CrewSerializer(ModelSerializer):
    image_thumbnail = ImageField(read_only=True)
    class Meta:
        model = Crew
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        ref_name = "User 1"