# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from accounts.forms import User
from accounts.models import UserProfile
from accounts.views import login_view
from comments.forms import CommentForm
from comments.models import Comment
from subjects.models import Subject, University, Degree, Center
from videos.models import Video

'''
def logged_in(request):
    if 'user' in request.session and request.user.is_authenticated:
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


def subject_detail(request, subject_id):
    # profile_instance = get_object_or_404(UserProfile, slug=slug)
    # user_ = None

    if request.user.is_authenticated:
        # user_ = get_object_or_404(UserProfile, user=request.user)
        user_ = UserProfile.objects.get(pk=request.user.id)
        # print(user_)
        subject = Subject.objects.get(pk=subject_id)
        videos = subject.videos_subjects.all()

        if request.POST:
            print('entrooo')
            user_.subjects.add(subject)
            user_.save()

        context = {
            'subject': subject,
            'videos': videos,
        }
        return render(request, "subject_detail.html", context)
    return redirect("login")


def subject_list(request):
    subjects = Subject.objects.all().order_by('name')

    context = {
        'subjects': subjects,
    }

    return render(request, "subject_list.html", context)


def subject_add(request, subject_id):
    user_ = UserProfile.objects.get(pk=request.user.id)
    subject = Subject.objects.get(pk=subject_id)
    user_.subjects.add(subject)
    user_.save()
    return redirect('subjects:subject_detail', subject_id)
