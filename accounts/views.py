from subjects.models import Subject
from videos.models import Video, UsersVideos
from .models import UserProfile
from comments.forms import CommentForm
from comments.models import Comment
#  from django.conf import settings
from django.db.models import Q
from django.contrib import messages

#  from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect  # Http404   HttpResponse

from django.views.generic import RedirectView
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

)
from .forms import UserLoginForm, UserRegisterForm, UserProfileForm


# Create your views here.
def profile_edit(request, slug=None):
    instance = get_object_or_404(UserProfile, slug=slug)
    form = UserProfileForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # message success
        messages.success(request, "item saved")
        return HttpResponseRedirect(instance.get_absolute_url())

    return render(request, "form.html", context={"form": form, "title": "edit"})


def profile_detail(request, slug=None):
    profile_instance = get_object_or_404(UserProfile, slug=slug)
    user_ = None
    if request.user.is_authenticated:
        user_ = request.user
    form = CommentForm(request.POST or None)
    if form.is_valid():
        content = form.cleaned_data.get("content")
        parent = None
        new_comment = Comment.objects.create(
            user=profile_instance,
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

        return HttpResponseRedirect(profile_instance.get_absolute_url())

    # qs_comments = Comment.objects.filter(user=profile_instance, parent=None) sin mensajes hijos
    qs_comments = Comment.objects.filter(user=profile_instance)

    qs_videos = Video.objects.filter(user=profile_instance)
    # qs_videos_comments = UsersVideos.objects.filter(video=qs_videos)
    # if qs_videos_comments:
    #    print ("qs_videos_comments")

    content = {
        "profile": profile_instance,
        'form': form,
        "comments": qs_comments,
        "videos": qs_videos,
        # "video_comments": qs_videos_comments,
        "user_": user_,
    }
    return render(request, "detail.html", content)


def profile_list(request):
    pass
    # qs = UserProfile.objects.all()
    # content = {
    #     "profiles": qs,
    # }
    # return render(request, "list.html", content)


def about(request):
    return render(request, "about.html")


def search(request):
    if request.user.is_authenticated:
        query = request.GET.get("search")
        user_ = request.user
        print(query)
        query_list = None
        if query:

            query_list = UserProfile.objects.filter(
                Q(username__icontains=query) |
                # Q(interests__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            ).distinct()
            if (query_list):
                context = {
                    'users': query_list,
                    'user_': user_,
                    'all_users': UserProfile.objects.all(),
                }
                return render(request, "search_profiles.html", context)

            if not query_list:

                query_list = Subject.objects.filter(name__icontains=query)
                if query_list:
                    context = {
                        'subjects': query_list,
                        'all_subjects': Subject.objects.all(),
                        'videos2': Video.objects.filter(subjectsvideos__subject__name=query),

                    }
                    return render(request, "search_subjects.html", context)

                elif not query_list:
                    query_list = Video.objects.filter(title__contains=query)
                    context = {
                        'videos2': query_list,
                        'all_videos': Video.objects.all(),
                        # 'videos2': Video.objects.filter(subjectsvideos__subject__name=query),

                    }
                    return render(request, "search_videos.html", context)
        print(query_list)

    else:
        return redirect("login")


def main_page(request):
    form = CommentForm(request.POST or None)
    query_list_users = None
    query_list_users_all = UserProfile.objects.all()
    # query_list_subjects = None
    user = request.user
    comments = None
    if user.is_authenticated:
        query_list_users = UserProfile.objects.filter(subjects__in=user.subjects.all()).exclude(pk=user.pk).distinct()
        comments = Comment.objects.filter(user__in=user.followers.all()).exclude(user=user)
        # query_list_subjects = Subject.objects.all()
    # print(query_list_subjects)

    # print(query_list_users)
    content = {
        "comments": comments,
        "user_": user,
        'form': form,
        "users": query_list_users,
        "all_users": query_list_users_all,
    }
    return render(request, "list.html", content)
    # return redirect("accounts:list")


class CommentLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        comment_id = self.kwargs.get("comment_id")
        # print(comment_id)
        comment_instance = get_object_or_404(Comment, id=comment_id)
        user = self.request.user
        url_ = user.get_absolute_url()
        if user.is_authenticated:
            if user in comment_instance.likes.all():
                comment_instance.likes.remove(user)
            else:
                comment_instance.likes.add(user)
        else:
            return "/login"
        return url_


class CommentUnLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        comment_id = self.kwargs.get("comment_id")
        # print(comment_id)
        comment_instance = get_object_or_404(Comment, id=comment_id)
        user = self.request.user
        url_ = user.get_absolute_url()
        if user.is_authenticated:
            if user in comment_instance.likes.all():
                comment_instance.unlikes.remove(user)
            else:
                comment_instance.unlikes.add(user)
        else:
            return "/login"
        return url_


class VideoLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        video_id = self.kwargs.get("video_id")
        # print(video_id)
        video_instance = get_object_or_404(Video, id=video_id)
        user = self.request.user
        url_ = "/videos/" + video_id + "/"
        # print(url_ + "/video/" + video_id + "/")

        if user.is_authenticated:
            if user in video_instance.likes.all():
                video_instance.likes.remove(user)
            else:
                video_instance.likes.add(user)
        else:
            return "/login"
        return url_


class VideoUnLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        video_id = self.kwargs.get("video_id")
        # print(video_id)
        video_instance = get_object_or_404(Video, id=video_id)
        user = self.request.user
        url_ = "/videos/" + video_id + "/"
        # print(url_ + "/video/" + video_id + "/")

        if user.is_authenticated:
            if user in video_instance.unlikes.all():
                video_instance.unlikes.remove(user)
            else:
                video_instance.unlikes.add(user)
        else:
            return "/login"
        return url_


class FollowToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            slug = self.kwargs.get("slug")
            # print(slug)
            user = self.request.user
            user_to_follow = UserProfile.objects.get(slug=slug)
            url_ = user.get_absolute_url()
            if user_to_follow in user.followers.all():
                user.followers.remove(user_to_follow)
            else:
                user.followers.add(user_to_follow)
            # print(user.followers.all())
            return user_to_follow.get_absolute_url()
        else:
            return "/login"


# Login & Logout & Registration Functions from Course try-django 1.9 not from me

def login_view(request):
    if not request.user.is_authenticated:
        # next = request.GET.get('next')
        title = "Login"
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            # if next:
            #     return redirect(next)
            return redirect("/")
        return render(request, "form.html", {"form": form, "title": title})
    else:
        redirect("/")


def register_view(request):
    if not request.user.is_authenticated:
        # next = request.GET.get('next')
        title = "Register"
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            new_user = authenticate(username=user.username, password=password)
            login(request, new_user)
            # if next:
            #     return redirect(next)
            return redirect("/")
    else:
        return redirect("/")
    context = {
        "form": form,
        "title": title
    }
    return render(request, "form.html", context)


def logout_view(request):
    logout(request)
    return redirect("/")


def uploadVideo(request):
    if (request.method == 'POST'):
        user_au = request.user
        new_video = Video(
            user=user_au,
            title=request.POST['title'],
            file=request.FILES.get('file'),
        )
        new_video.save(),

        # video = new_video,
        print(request.POST['subjects'])
        subject = Subject.objects.get(id=request.POST['subjects'])
        new_video.subjects.add(subject)

        # new_subject_video.save(),

    subjects = Subject.objects.all()
    content = {
        'subjects': subjects,

    }
    return render(request, 'videoupload.html', content)


'''
def exshow(request, slug, video_id):
    videos = get_object_or_404(Video, pk=video_id)
    # videos2 = Video.objects.filter(title=title)
    # comments = UsersVideos.objects.filter(user__video__title__icontains=title)

    content = {
        'videos': videos,
    }
    return render(request, 'items/videos.html', content)
'''


def list_subjects(request):
    subjects = Subject.objects.all()
    content = {
        'subjects': subjects,
    }
    return render(request, 'items/subjects.html', content)
