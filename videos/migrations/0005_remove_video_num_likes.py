# Generated by Django 2.2.3 on 2019-10-11 00:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_video_num_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='num_likes',
        ),
    ]