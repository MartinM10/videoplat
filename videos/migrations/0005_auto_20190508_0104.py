# Generated by Django 2.2 on 2019-05-07 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_auto_20190508_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='views',
            field=models.BigIntegerField(blank=True, default=0, null=True),
        ),
    ]