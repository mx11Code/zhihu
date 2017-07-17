# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-16 16:32
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20170716_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='register_email',
            field=models.EmailField(default='', max_length=254, validators=[django.core.validators.EmailValidator()]),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=30, validators=[user.models.validate_is_blank]),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=30, unique=True, validators=[user.models.validate_is_blank]),
        ),
    ]