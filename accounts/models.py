from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


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
    objects = UserManager()

    email = models.EmailField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    name = models.CharField('이름', max_length=20, null=True, blank=True)
    created_date = models.DateTimeField('등록일자', auto_now_add=True)
    updated_date = models.DateTimeField('수정일자', auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin
