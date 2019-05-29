# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

# Create your views here.
from comments.forms import CommentForm
from comments.models import Comment
from videos.models import Video, UserVideo


def showVideo(request, video_id):
    user = request.user
    video = get_object_or_404(Video, pk=video_id)
    # videos2 = Video.objects.filter(title=title)
    # comments = UsersVideos.objects.filter(user__video__title__icontains=title)
    views = video.views
    print(views)
    video.views = views + 1
    form = CommentForm(request.POST or None)
    if form.is_valid():
        content = form.cleaned_data.get("content")
        parent = None
        new_comment = Comment.objects.create(
            user=user,
            content=content,
            parent=parent,
        )
        try:
            parent = int(request.POST.get("parent_id"))
        except:
            parent = None
        if parent:
            new_comment.parent = Comment.objects.filter(id=parent).first()

        new_comment.save()
        video.comments = video.comments + 1
        UserVideo.objects.update_or_create(user=user, video=video, comments=new_comment)

    video.save()
    comments = UserVideo.objects.filter(video_id=video_id).order_by('comments__added').reverse()

    context = {
        'user': user,
        'video': video,
        'comments': comments,
        'form': form,
    }
    return render(request, 'items/videos.html', context)
