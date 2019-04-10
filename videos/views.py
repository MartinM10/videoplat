# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

# Create your views here.
from videos.models import Video


def showVideo(request, video_id):
    video = get_object_or_404(Video, pk=video_id)

    # videos2 = Video.objects.filter(title=title)
    # comments = UsersVideos.objects.filter(user__video__title__icontains=title)

    context = {
        'video': video,
    }
    return render(request, 'items/videos.html', context)
