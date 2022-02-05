from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User
from common.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Crew(models.Model):

    class MeetingType(models.TextChoices):
        ONLINE = '온라인', _('온라인')
        OFFLINE = '오프라인', _('오프라인')
        ON_OFFLINE = '온/오프라인', _('온/오프라인')

    class CommunityType(models.TextChoices):
        FIRST = '1청년부', _('1청년부')
        SECOND = '2청년부', _('2청년부')
        THIRD = '3청년부', _('3청년부')
        MARRIED = '신혼브릿지', _('신혼브릿지')

    name = models.CharField('크루명', max_length=30)
    description = models.TextField('한줄소개')
    create_date = models.DateTimeField('크루 생성날짜', default=timezone.now)
    meeting_type = models.CharField('모임형태',max_length=6, choices=MeetingType.choices, default=MeetingType.ON_OFFLINE)
    meeting_time = models.CharField('모임시간',max_length=20)
    community = models.CharField('크루 소속 공동체',max_length=6, choices=CommunityType.choices, default=CommunityType.FIRST)

    manager = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='크루매니저', related_name='manager')

    members = models.ManyToManyField(User,related_name='members')

    member_limit = models.PositiveSmallIntegerField("최대 모임 인원",default=5, help_text="5~15명 이내로 설정해주세요")


    class Meta:
        ordering = ['-id']

