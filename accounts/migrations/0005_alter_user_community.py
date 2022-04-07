# Generated by Django 4.0.2 on 2022-04-07 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='community',
            field=models.IntegerField(choices=[(0, '1청년부'), (1, '2청년부'), (2, '3청년부'), (3, '신혼브릿지'), (4, '기타')], default=0, verbose_name='소속 공동체'),
        ),
    ]
