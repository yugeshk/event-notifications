# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-12 18:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0020_auto_20171012_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercategory',
            name='categoryId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Category'),
        ),
    ]
