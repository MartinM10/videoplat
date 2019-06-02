# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from comments.forms import CommentForm
from comments.models import Comment
from videos.forms import UserAdvancedSearchVideoForm
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


def advanced_search_videos(request):
    if request.user.is_authenticated:
        if request.POST:
            form = UserAdvancedSearchVideoForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                user = form.cleaned_data.get('user')
                description = form.cleaned_data.get('description')
                likes = form.cleaned_data.get('likes')
                dislikes = form.cleaned_data.get('dislikes')
                views = form.cleaned_data.get('views')
                subjects = form.cleaned_data.get('subjects')

                query_video = Video.objects.filter(title__icontains=title,
                                                   user__in=user,
                                                   description__icontains=description,
                                                   likes=likes,
                                                   dislikes=dislikes,
                                                   views__gt=views,
                                                   subjects__name__icontains=subjects)
                print(query_video)
                context = {'videos': query_video, 'form': form}
                return render(request, "advanced_search_videos.html", context)

        else:
            query = request.GET.get("search")
            query_video = Video.objects.filter(title__icontains=query)
            if query_video:
                print(query_video)
            print(query)
            form = UserAdvancedSearchVideoForm()
            context = {'videos': query_video, 'form': form}
            return render(request, "advanced_search_videos.html", context)

    else:
        return redirect("login")
