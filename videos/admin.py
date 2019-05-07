# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
import subjects.models
from videos.models import Video, UserVideo  # , UsersVideos


class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'file']


# ¿ o pongo list_display = ['title', 'user']
admin.site.register(Video, VideoAdmin)


class VideosUsersAdmin(admin.ModelAdmin):
    list_display = ['video', 'user']


admin.site.register(UserVideo, VideosUsersAdmin)

'''
class VideosSubjectsAdmin(admin.ModelAdmin):
    list_display = ['video', 'subject']


admin.site.register(VideosSubjectsAdmin)
'''
# admin.site.register(SubjectsVideos)
# admin.site.register(UsersVideos)
