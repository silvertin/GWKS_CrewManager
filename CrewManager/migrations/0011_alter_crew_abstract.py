# Generated by Django 4.0.2 on 2022-04-07 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CrewManager', '0010_crew_community_limit_alter_crew_community'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crew',
            name='abstract',
            field=models.CharField(max_length=30, verbose_name='크루한줄설명'),
        ),
    ]
