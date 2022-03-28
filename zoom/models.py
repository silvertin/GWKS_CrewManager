from django.db import models
from django.utils import timezone

from accounts.models import User

from django_jsonform.models.fields import JSONField

# Create your models here.

MEETING_TYPE_CHOICES = [
    (1, '일반'),
    (2, '예약'),
    (3, '반복'),
    (8, '반복예약')
]

SETTINGS_SCHEMA = {
    'type': 'dict',
    'keys': {
        'alternative_hosts': {
            'type': 'string',
            'title': '대체 호스트 지정',
            'format': 'email',
            'default': ''
        },
        "alternative_hosts_email_notification": {
            'type': 'boolean',
            'title': '대체 호스트 이메일 알림',
            'default': True
        },
        "breakout_room": {
            'type': 'dict',
            'title': '소회의실 설정',
            'keys': {
                "enable": {
                    'type': 'boolean',
                    'title': '소회의실 설정 여부',
                    'default': False
                },
                "rooms": {
                    'type': 'list',
                    'title': '소회의실 리스트',
                    'default': [],
                    'items': {
                        'type': 'dict',
                        'keys': {
                            'name': {
                                'type': 'string',
                                'title': '소회의실 이름',
                                'default': ''
                            },
                            'participants': {
                                'type': 'list',
                                'title': '소회의실 참석자 리스트',
                                'default': [],
                                'items': {
                                    'type': 'string',
                                    'default': '',
                                    'format': 'email'
                                }
                            }

                        }
                    }
                }
            }
        },
        "meeting_invitees": {
            'type': 'list',
            'title': '참석자 리스트',
            'default': [],
            'items': {
                'email': {
                    'type': 'string',
                    'title': '참석자 이메일',
                    'format': 'email',
                    'default': ''
                }
            }
        },
        "mute_upon_entry": {
            'type': 'boolean',
            'title': '입장시 음소거',
            'default': True
        },
        "participant_video": {
            'type': 'boolean',
            'title': '입장시 비디오 On',
            'default': True
        },
        "private_meeting": {
            'type': 'boolean',
            'title': '비공개 회의',
            'default': False
        },
        "waiting_room": {
            'type': 'boolean',
            'title': '대기실 On',
            'default': False
        }
    }
}


class ZoomAccount(models.Model):
    name = models.CharField('계정 이름', max_length=30)
    description = models.TextField('설명')
    create_date = models.DateTimeField('등록날짜', default=timezone.now)
    available = models.BooleanField('사용가능', default=False)
    appkey = models.CharField('키', max_length=30)
    secretkey = models.CharField('비밀 키', max_length=60)
    useremail = models.EmailField('사용자 이메일')

    def __str__(self):
        return self.name

class ZoomMeeting(models.Model):
    meetingid = models.IntegerField('id', default=0)
    topic = models.CharField('모임 주제',max_length=60)
    description = models.TextField('모임 설명', null=True, blank=True)
    type_meeting = models.PositiveSmallIntegerField('모임 타입', default=1, choices=MEETING_TYPE_CHOICES)
    create_dt = models.DateTimeField('등록날짜', default=timezone.now)
    start_dt = models.DateTimeField('시작시간',null=True, blank=True)
    duration = models.PositiveIntegerField('진행 시간')
    password = models.CharField('비밀번호', max_length=10, default='')
    join_url = models.URLField('모임 URL', default='')
    account = models.ForeignKey(ZoomAccount, on_delete=models.PROTECT, blank=True, null=True, verbose_name='줌 계정', related_name='account')
    user = models.ForeignKey(User, verbose_name='사용자', on_delete=models.PROTECT, blank=True, null=True)
    settings = JSONField(schema=SETTINGS_SCHEMA,null=True, blank=True)

    def __str__(self):
        return self.topic

