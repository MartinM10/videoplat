# Generated by Django 2.1.2 on 2019-04-07 22:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comments', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subjects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectsVideos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subjects.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='UsersVideos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seconds_watched', models.IntegerField(default=0)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('comments', models.ManyToManyField(blank=True, related_name='video_comments', to='comments.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_videos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('file', models.FileField(upload_to='video_folder/')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('watched', models.BooleanField(default=False)),
                ('views', models.BigIntegerField(default=0)),
                ('likes', models.ManyToManyField(blank=True, related_name='videos_liked', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank='True', null=True, on_delete=django.db.models.deletion.SET_NULL, to='videos.Video')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'video',
                'ordering': ['-added'],
            },
        ),
        migrations.AddField(
            model_name='usersvideos',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_videos', to='videos.Video'),
        ),
        migrations.AddField(
            model_name='subjectsvideos',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.Video'),
        ),
        migrations.AlterUniqueTogether(
            name='usersvideos',
            unique_together={('user', 'video')},
        ),
        migrations.AlterUniqueTogether(
            name='subjectsvideos',
            unique_together={('subject', 'video')},
        ),
    ]
