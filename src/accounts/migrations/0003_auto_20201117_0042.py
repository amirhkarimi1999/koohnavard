# Generated by Django 3.1.2 on 2020-11-17 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20201114_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to='profile_pics', verbose_name='عکس پروفایل'),
        ),
    ]
