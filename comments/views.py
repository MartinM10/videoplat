# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from accounts.models import UserProfile
from comments.models import Comment
from videos.models import Video


def index(request):
    comment = Comment.objects.order_by('-pk')[0]
    comments = Comment.objects.all()

    context = {
        "comments": comments,
        "comment": comment,
    }

    return render(request, 'index.html', context)
