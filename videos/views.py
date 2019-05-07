# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

# Create your views here.
from videos.models import Video, UserVideo


def showVideo(request, video_id):
    user = request.user
    video = get_object_or_404(Video, pk=video_id)
    comments = UserVideo.objects.filter(video_id=video_id)
    # videos2 = Video.objects.filter(title=title)
    # comments = UsersVideos.objects.filter(user__video__title__icontains=title)

    context = {
        'user': user,
        'video': video,
        'comments': comments
    }
    return render(request, 'items/videos.html', context)
