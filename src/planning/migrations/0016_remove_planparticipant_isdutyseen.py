# Generated by Django 3.1.4 on 2021-01-05 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0015_auto_20210105_1747'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planparticipant',
            name='isDutySeen',
        ),
    ]