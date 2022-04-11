from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User
from accounts.models import User
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit

from multiselectfield import MultiSelectField



# Create your models here.
class Crew(models.Model):

    class MeetingType(models.TextChoices):
        ONLINE = '온라인', _('온라인')
        OFFLINE = '오프라인', _('오프라인')
        ON_OFFLINE = '온/오프라인', _('온/오프라인')

    # class CommunityType(models.TextChoices):
    #     FIRST = '1청년부', _('1청년부')
    #     SECOND = '2청년부', _('2청년부')
    #     THIRD = '3청년부', _('3청년부')
    #     MARRIED = '신혼브릿지', _('신혼브릿지')

    class WeekDayType(models.TextChoices):
        MONDAY = '월요일', _('월요일')
        TUESDAY = '화요일', _('화요일')
        WEDNESDAY = '수요일', _('수요일')
        THURSDAY = '목요일', _('목요일')
        FRIDAY = '금요일', _('금요일')
        SATURDAY = '토요일', _('토요일')
        SUNDAY = '일요일', _('일요일')
        NODAY = '선택안함', _('선택안함')

    class PeriodType(models.TextChoices):
        ONEWEEK = '매주', _('매주')
        TWOWEEK = '격주', _('격주')
        NOWEEK = '선택안함', _('선택안함')

    name = models.CharField('크루명 (30자 이내)', max_length=30)
    abstract = models.CharField('크루한줄설명 (30자 이내)', max_length=30)
    description = RichTextUploadingField('크루 설명 (모바일에 들어갈 사이즈입니다. 줄바꿈 확인필요, 이미지 업로드 가능)',blank=True, null=True)
    create_date = models.DateTimeField('크루 생성날짜', default=timezone.now)
    meeting_type = models.CharField('모임형태',max_length=6, choices=MeetingType.choices, default=MeetingType.ON_OFFLINE)

    meeting_time = models.CharField('기타 모임시간 (나중에 시간을 정해야한다면 여기다 적어주세요)',max_length=30)

    weekday = models.CharField('모임 요일', max_length=4, choices=WeekDayType.choices, default=WeekDayType.NODAY)
    period = models.CharField('모임 반복 주기', max_length=4, choices=PeriodType.choices, default=PeriodType.NOWEEK)
    start_time = models.TimeField('모임 시작 시간 (19:00 와 같은 형식으로 적어주세요)', blank=True, null=True)
    end_time = models.TimeField('모임 종료 시간 (21:00 와 같은 형식으로 적어주세요)', blank=True, null=True)



    meeting_limit = models.CharField('모임제한 (특별히 이런 사람들이 왔으면 좋겠다 같은 내용,30자 이내)',max_length=30)
    # community = models.CharField('크루 소속 공동체',max_length=6, choices=CommunityType.choices, default=CommunityType.FIRST)
    community = models.IntegerField('크루 소속 공동체 (크루리더가 소속된 공동체 = 예산사용공동체)', choices=User.CommunityType.choices, default=User.CommunityType.FIRST)
    community_limit = MultiSelectField('크루원 참여 공동체 제한',choices=User.CommunityType.choices, null=True, blank=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='크루매니저', related_name='manager')

    members = models.ManyToManyField(User,related_name='members')

    member_limit = models.PositiveSmallIntegerField("최대 모임 인원 (본인 포함)",default=5, help_text="5~15명 이내로 설정해주세요", validators=[MinValueValidator(5), MaxValueValidator(60)])
    image = ProcessedImageField(verbose_name='크루 소개 이미지 (정사각형, 500x500이상)',upload_to='crew/resize/%y%m%d',
                              processors=[ResizeToFit(width=500,height=500,upscale=False)],
                              format='JPEG', null=True, blank=True)
    image_thumbnail = ImageSpecField(source='image', processors=[ResizeToFit(width=200,height=200,upscale=False)],
                                                                 format='JPEG',
                                     options={'quality':60})

    kakao_room = models.URLField('오픈카톡방 URL',null=True, blank=True)


    class Meta:
        ordering = ['-id']

