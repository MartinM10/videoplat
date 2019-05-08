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
    user = models.ForeignKey('accounts.UserProfile', on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='video_folder/')
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey("self", null=True, blank="True", on_delete=models.SET_NULL)
    likes = models.ManyToManyField('accounts.UserProfile', blank=True, related_name="videos_likes")
    unlikes = models.ManyToManyField('accounts.UserProfile', blank=True, related_name="videos_unlikes")
    views = models.BigIntegerField(null=True, blank=True, default=0)
    subjects = models.ManyToManyField(Subject, blank=True, related_name="videos_subjects")

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
        return reverse("accounts:like_video_toggle", kwargs={"video_id": self.id})

    def get_unlike_url(self):
        return reverse("accounts:unlike_video_toggle", kwargs={"video_id": self.id})

    def get_like_instances(self):
        return self.likes.all()

    def get_unlike_instances(self):
        return self.unlikes.all()

    def get_user_object(self):
        return get_object_or_404(UserProfile, user=self.user)

    def get_image_url(self):
        user_ = get_object_or_404(UserProfile, user=self.user)
        return user_.image.url


class UserVideo(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="users_videos")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="users_videos")
    watched = models.BooleanField(default=False)
    seconds_watched = models.IntegerField(default=0)
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name="video_comments")
    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('user', 'video'),)

    def __str__(self):
        return '{}' " - " '{}'.format(self.user, self.video)


'''
class SubjectsVideos(models.Model):
    subject = models.ForeignKey(Subject, models.CASCADE)
    video = models.ForeignKey(Video, models.CASCADE)

    class Meta:
        unique_together = (('subject', 'video'),)

    def get_name_subject(self):
        return self.subject.name

    def get_title_video(self):
        return self.video.title
'''
# tema = models.CharField(max_length=45, blank=True, null=True)
# examen = models.CharField(max_length=45, blank=True, null=True)
