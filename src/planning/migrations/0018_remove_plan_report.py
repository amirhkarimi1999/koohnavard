# Generated by Django 3.1.4 on 2021-01-07 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0017_planpicture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='report',
        ),
    ]
