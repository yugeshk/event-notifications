# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-10 19:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_publishersettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='publishersettings',
            name='verifiedPublisher',
            field=models.CharField(default='false', max_length=5),
        ),
    ]
