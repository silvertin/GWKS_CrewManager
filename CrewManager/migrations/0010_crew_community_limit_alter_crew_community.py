# Generated by Django 4.0.2 on 2022-04-07 12:58

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('CrewManager', '0009_crew_end_time_crew_period_crew_start_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='crew',
            name='community_limit',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(0, '1청년부'), (1, '2청년부'), (2, '3청년부'), (3, '신혼브릿지'), (4, '기타')], max_length=9, null=True, verbose_name='크루원 참여 공동체 제한'),
        ),
        migrations.AlterField(
            model_name='crew',
            name='community',
            field=models.IntegerField(choices=[(0, '1청년부'), (1, '2청년부'), (2, '3청년부'), (3, '신혼브릿지'), (4, '기타')], default=0, verbose_name='크루 소속 공동체'),
        ),
    ]
