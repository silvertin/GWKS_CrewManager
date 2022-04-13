# Generated by Django 4.0.2 on 2022-04-13 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CrewManager', '0014_crew_kakao_room_alter_crew_member_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crew',
            name='community',
            field=models.IntegerField(choices=[(0, '1청년부'), (1, '2청년부'), (2, '3청년부'), (3, '신혼브릿지'), (4, '기타')], default=4, verbose_name='크루 소속 공동체 (크루리더가 소속된 공동체 = 예산사용공동체)'),
        ),
    ]
