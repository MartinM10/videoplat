# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404

# Create your views here.
from accounts.forms import User
from accounts.models import UserProfile
from accounts.views import login_view
from comments.forms import CommentForm
from comments.models import Comment
from subjects.models import Subject
from videos.models import SubjectsVideos

'''
def logged_in(request):
    if 'user' in request.session and request.user.is_authenticated():
        subjects = Subject.objects.all()
        return render(request, 'main.html', {'subjects': subjects})
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            return render(request, 'register_view.html', {'error_message': 'Please Register First'})
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login_view(request, user)
                request.session['user'] = username
                subjects = Subject.objects.all()
                return render(request, 'main.html', {'subjects': subjects})
            else:
                return render(request, 'login_view.html', {'error_message': 'Your Account Has Been Suspended'})
        return render(request, 'login_view.html', {'error_message': 'Wrong Credentials'})
    return render(request, 'login_view.html')



def list_subjects(request):
    subject = Subject.objects.all()
    return render(request, template_name='items/subjects.html', context={'subject': subject})
'''


def subject_detail(request, name):
    # profile_instance = get_object_or_404(UserProfile, slug=slug)
    # user_ = None

    if request.user.is_authenticated:
        # user_ = get_object_or_404(UserProfile, user=request.user)
        # query = request.GET.get("search")

        subject = Subject.objects.filter(name__icontains=name)
        videos = SubjectsVideos.objects.filter(subject__name__icontains=name)

        context = {
            'subjects': subject,
            'videos': videos,
        }

    return render(request, "subject_detail.html", context)


def subject_list(request):
    return render(request, "subject_list.html", {'subjects': Subject.objects.all()})
