# Generated by Django 3.1.2 on 2021-02-19 08:28

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('planning', '0018_remove_plan_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.date.today, verbose_name='start_datetime'),
        ),
    ]