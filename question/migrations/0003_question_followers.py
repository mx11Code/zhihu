# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-21 23:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('question', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='followers',
            field=models.ManyToManyField(related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
    ]