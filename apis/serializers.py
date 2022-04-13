from rest_framework.serializers import ModelSerializer, ImageField, HyperlinkedModelSerializer
from CrewManager.models import Crew
from accounts.models import User
from rest_framework import fields

class CrewSerializer(ModelSerializer):
    image_thumbnail = ImageField(read_only=True)
    community_limit = fields.MultipleChoiceField(choices=User.CommunityType.choices)
    class Meta:
        model = Crew
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','last_login','email','is_active','name','nickname','birthyear','community','profile_image', 'is_superuser','is_admin']
        ref_name = "User 1"