# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models

# Create your models here.
from django.shortcuts import get_object_or_404
from django.urls import reverse

from accounts.models import UserProfile
from comments.models import Comment
from subjects.models import Subject


class Video(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='video_folder/')
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    watched = models.BooleanField(default=False)
    parent = models.ForeignKey("self", null=True, blank="True")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                   related_name="video_likes")
    views = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'video'
        ordering = ['-added']

    def __str__(self):
        return '{}' " || " '{}'.format(self.title, self.user)

    def children(self):
        return Video.objects.filter(parent=self)

    def get_name_subject(self):
        return self.video_set

    def get_like_url(self):
        return reverse("accounts:like_toggle", kwargs={"video_id": self.id})

    def get_like_instances(self):
        return self.likes.all()

    def get_user_object(self):
        return get_object_or_404(UserProfile, user=self.user)

    def get_image_url(self):
        user_ = get_object_or_404(UserProfile, user=self.user)
        return user_.image.url


class UsersVideos(models.Model):
    user = models.ForeignKey(UserProfile, models.CASCADE)
    video = models.ForeignKey(Video, models.CASCADE)
    seconds_watched = models.IntegerField(default=0)
    comment = models.ManyToManyField(Comment, blank=True, related_name="video_coments")
    timestamp = models.DateTimeField(auto_now=True)

    '''
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                   related_name="video_likes")
    '''

    class Meta:
        db_table = 'users_videos'
        unique_together = (('user', 'video'),)

    def __str__(self):
        return '{}' " - " '{}'.format(self.user, self.video)


class SubjectsVideos(models.Model):
    subject = models.ForeignKey(Subject, models.CASCADE)
    video = models.ForeignKey(Video, models.CASCADE)

    class Meta:
        db_table = 'subjects_videos'
        unique_together = (('subject', 'video'),)

    def get_name_subject(self):
        return self.subject.name

    def get_title_video(self):
        return self.video.title

    # tema = models.CharField(max_length=45, blank=True, null=True)
    # examen = models.CharField(max_length=45, blank=True, null=True)
