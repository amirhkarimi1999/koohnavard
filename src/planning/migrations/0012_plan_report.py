# Generated by Django 3.1.3 on 2020-12-26 20:29

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0011_auto_20201226_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='report',
            field=markdownx.models.MarkdownxField(null=True),
        ),
    ]