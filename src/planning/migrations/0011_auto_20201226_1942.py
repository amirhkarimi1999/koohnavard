# Generated by Django 3.1.3 on 2020-12-26 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0010_auto_20201226_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charge',
            name='amount',
            field=models.DecimalField(decimal_places=0, max_digits=20, verbose_name='amount'),
        ),
    ]