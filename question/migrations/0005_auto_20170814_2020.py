# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-14 20:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0004_auto_20170721_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tag',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
