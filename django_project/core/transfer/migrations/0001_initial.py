# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-03-31 15:57
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('layers', '0032_auto_20180424_1638'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=20)),
                ('filepath', models.FileField(blank=True, null=True, upload_to=b'')),
                ('is_finished', models.BooleanField(default=False)),
                ('created', models.DateTimeField(default=datetime.datetime(2019, 3, 31, 15, 57, 53, 398349, tzinfo=utc))),
                ('errors', models.TextField(blank=True, null=True)),
                ('output_logs', models.TextField(blank=True, null=True)),
                ('designated_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('layer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='layers.Layer')),
            ],
        ),
    ]
