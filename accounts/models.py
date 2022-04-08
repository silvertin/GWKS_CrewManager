from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email,name, password):
        if not email:
            raise ValueError('이메일을 적어주셔야 합니다.')
        if not password:
            raise ValueError('비밀번호를 적어주셔야 합니다.')

        user = self.model(email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,name, password):
        user = self.create_user(email=self.normalize_email(email), name=name, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):

    class CommunityType(models.IntegerChoices):
        FIRST = 0, _('1청년부')
        SECOND = 1, _('2청년부')
        THIRD = 2, _('3청년부')
        MARRIED = 3, _('신혼브릿지')
        ETC = 4, _('기타')

    objects = UserManager()

    email = models.EmailField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    name = models.CharField('이름', max_length=20, null=True, blank=True)
    nickname = models.CharField('닉네임', max_length=20, null=True, blank=True)
    birthyear = models.PositiveSmallIntegerField('또래', null=True ,validators=[MinValueValidator(0), MaxValueValidator(99)])
    #community = models.CharField('소속 공동체',max_length=6, choices=CommunityType.choices, default=CommunityType.FIRST)
    community = models.IntegerField('소속 공동체', choices=CommunityType.choices, default=CommunityType.FIRST)

    created_date = models.DateTimeField('등록일자', auto_now_add=True)
    updated_date = models.DateTimeField('수정일자', auto_now=True)

    profile_image = models.URLField('프로파일이미지URL', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin
