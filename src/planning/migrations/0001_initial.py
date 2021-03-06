# Generated by Django 3.0.4 on 2020-11-13 23:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('participation', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=50)),
                ('description', models.CharField(default='', max_length=256)),
                ('destination_address', models.CharField(default='', max_length=256)),
                ('start_datetime', models.DateTimeField()),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='participation.Club')),
            ],
        ),
        migrations.CreateModel(
            name='PlanParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')], max_length=255)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planning.Plan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
