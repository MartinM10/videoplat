# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404
from accounts.models import UserProfile


# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey('accounts.UserProfile', on_delete=models.CASCADE, default=1, related_name="transmitter")
    content = models.TextField(null=False, blank=False)
    added = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    likes = models.ManyToManyField('accounts.UserProfile', blank=True, related_name="comment_likes")
    dislikes = models.ManyToManyField('accounts.UserProfile', blank=True, related_name="comment_dislikes")
    user2 = models.ForeignKey('accounts.UserProfile', default=1, blank=True, related_name="receiver",
                              on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['-added']

    def children(self):
        return Comment.objects.filter(parent=self)

    def __str__(self):
        return '{}' " || " '{}' " || " '{}'.format(self.user, self.id, self.added)

    def get_like_url(self):
        return reverse("accounts:like_toggle", kwargs={"comment_id": self.id})

    def get_dislike_url(self):
        return reverse("accounts:dislike_toggle", kwargs={"comment_id": self.id})

    def get_like_instances(self):
        return self.likes.all()

    def get_dislike_instances(self):
        return self.dislikes.all()

    def get_user_object(self):
        return self.user

    def get_image_url(self):
        user_ = self.user
        return user_.image.url
