# Generated by Django 2.2 on 2019-04-08 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190408_0044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='interests',
        ),
    ]
