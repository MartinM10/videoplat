# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-04-04 20:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_auto_20190402_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='views',
            field=models.BigIntegerField(default=0),
        ),
    ]
