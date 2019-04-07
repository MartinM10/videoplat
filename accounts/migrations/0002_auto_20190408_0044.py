# Generated by Django 2.1.2 on 2019-04-07 22:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='_userprofile_followers_+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='subjects',
            field=models.ManyToManyField(blank=True, related_name='users', to='subjects.Subject'),
        ),
    ]
