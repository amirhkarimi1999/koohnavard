# Generated by Django 3.1.3 on 2020-12-25 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0006_planparticipant_duty'),
    ]

    operations = [
        migrations.AddField(
            model_name='planparticipant',
            name='isDutySeen',
            field=models.BooleanField(default=False, verbose_name='isDutyseen'),
        ),
    ]
