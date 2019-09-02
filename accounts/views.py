from star_ratings import get_star_ratings_rating_model

from subjects.models import Subject
from videos.models import Video, UserVideo
from .models import UserProfile, RatingUser
from comments.forms import CommentForm
from comments.models import Comment
#  from django.conf import settings
from django.db.models import Q, Count
from django.contrib import messages

from itertools import chain

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
from .forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserAdvancedSearchUserForm, \
    UserAdvancedSearchSubjectForm, UserAdvancedSearchVideoForm, UserDisplayForm


# Create your views here.
def profile_edit(request, slug=None):
    instance = get_object_or_404(UserProfile, slug=slug)
    top3users = UserProfile.objects.order_by('followers').reverse()[:3]
    top3videosviews = Video.objects.order_by('views').reverse()[:3]
    top3videoslikes = Video.objects.order_by('likes').reverse()[:3]
    form = UserProfileForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save()
        instance.save()
        # form.save_m2m
        # message success
        messages.success(request, "Guardado correctamente")
        return HttpResponseRedirect(instance.get_absolute_url())

    return render(request, "form.html", context={"form": form, "title": "Editar perfil", })


def profile_detail(request, slug=None):
    profile_instance = get_object_or_404(UserProfile, slug=slug)
    user_ = None
    if request.user.is_authenticated:
        user_ = request.user

    instance_rating = RatingUser.objects.filter(user_rated=profile_instance, user_rating=request.user).first()
    votes = RatingUser.objects.filter(user_rated=profile_instance).count()

    form = CommentForm(request.POST or None)
    form_user = UserDisplayForm(request.GET or None, request.GET or None, instance=profile_instance)

    if form.is_valid():
        content = form.cleaned_data.get("content")
        parent = None
        new_comment = Comment.objects.create(
            user=user_,
            user2=profile_instance,
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
    qs_comments = Comment.objects.filter(user2=profile_instance)

    qs_videos = Video.objects.filter(user=profile_instance)

    if instance_rating:
        context = {
            "profile": profile_instance,
            'form': form,
            'formUser': form_user,
            "comments": qs_comments,
            "videos": qs_videos,
            # "video_comments": qs_videos_comments,
            "user_": user_,
            'rating_average': profile_instance.get_average_rating(),
            'rating_vote': instance_rating.vote,
            'votes': votes
        }
    else:
        context = {
            "profile": profile_instance,
            'form': form,
            'formUser': form_user,
            "comments": qs_comments,
            "videos": qs_videos,
            # "video_comments": qs_videos_comments,
            "user_": user_,
            'rating_average': profile_instance.get_average_rating(),
            'votes': votes
        }
    return render(request, "detail.html", context)


def profile_list(request):
    pass
    # qs = UserProfile.objects.all()
    # content = {
    #     "profiles": qs,
    # }
    # return render(request, "list.html", content)


def about(request):
    return render(request, "about.html")


'''
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
            if query_list:
                context = {
                    'users': query_list,
                    'user_': user_,
                    'all_users': UserProfile.objects.all(),
                }
                return render(request, "search_profiles.html", context)

            if not query_list:

                # query_list = Subject.objects.filter(name__icontains=query)
                query_list = Subject.objects.filter(name__icontains=query)
                if query_list:
                    videos = Video.objects.filter(subjects__id=query_list.id)

                if query_list:
                    context = {
                        'subject': query_list,
                        'all_subjects': Subject.objects.all(),
                        'videos': videos,

                    }
                    return render(request, "search_subjects.html", context)

                elif not query_list:
                    query_list = Video.objects.filter(title__contains=query)
                    for vid in query_list:
                        video = get_object_or_404(Video, id=vid.id)
                        comments = UserVideo.objects.filter(video_id=video.id)

                    # videos2 = Video.objects.filter(title=title)
                    # comments = UsersVideos.objects.filter(user__video__title__icontains=title)
                    views = video.views
                    print(views)
                    video.views = views + 1
                    video.save()
                    form = CommentForm(request.POST or None)
                    if form.is_valid():
                        content = form.cleaned_data.get("content")
                        parent = None
                        new_comment = Comment.objects.create(
                            user=user_,
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
                    context = {
                        'user:': user_,
                        'videos': query_list,
                        'all_videos': Video.objects.all(),
                        'comments': comments,
                        'form': form,
                        # 'videos2': Video.objects.filter(subjectsvideos__subject__name=query),

                    }
                    return render(request, "search_videos.html", context)
        print(query_list)

    else:
        return redirect("login")
'''


def search(request):
    if request.user.is_authenticated:
        query = request.GET.get("search")
        user_ = request.user
        print(query)
        query_list = None
        if query:
            query_user = UserProfile.objects.filter(
                Q(username__icontains=query) |
                # Q(interests__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            ).distinct()
            query_subject = Subject.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)).distinct()
            query_video = Video.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).distinct()
            query_comment_video = UserVideo.objects.filter(comments__content__icontains=query).distinct()
            query_comment = Comment.objects.filter(content__icontains=query).distinct()

            # merge Querysets from different models
            result_list = list(chain(query_user, query_subject, query_video, query_comment_video, query_comment))

            # si alguna de las queries anteriores tiene datos
            context = {'users': query_user, 'subjects': query_subject, 'videos': query_video,
                       'comments_videos': query_comment_video, 'comments': query_comment, }
            return render(request, "search.html", context)

    else:
        return redirect("login")


def advanced_search_users(request):
    if request.user.is_authenticated:
        if request.POST:
            form = UserAdvancedSearchUserForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                followers = form.cleaned_data.get('followers')
                subjects = form.cleaned_data.get('subjects')

                query_user = UserProfile.objects.all()

                if username:
                    query_user = query_user.filter(username__icontains=username)
                if first_name:
                    query_user = query_user.filter(first_name__icontains=first_name)
                if last_name:
                    query_user = query_user.filter(last_name__icontains=last_name)
                if email:
                    query_user = query_user.filter(email__icontains=email)
                if followers:
                    query_user = query_user.filter(followers=followers)
                if subjects:
                    query_user = query_user.filter(subjects__name__icontains=subjects)

                context = {'users': query_user, 'form': form}
                return render(request, "advanced_search_users.html", context)

        else:
            # query = request.GET.get("search")
            # query_user = UserProfile.objects.filter(username__icontains=query)
            query_user = UserProfile.objects.all().order_by('username')
            form = UserAdvancedSearchUserForm()
            context = {'users': query_user, 'form': form}
            return render(request, "advanced_search_users.html", context)

    else:
        return redirect("login")


def advanced_search_subjects(request):
    if request.user.is_authenticated:
        if request.POST:
            form = UserAdvancedSearchSubjectForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                course = form.cleaned_data.get('course')
                degree = form.cleaned_data.get('degree')
                center = form.cleaned_data.get('center')
                university = form.cleaned_data.get('university')
                validated = form.cleaned_data.get('validated')

                query_subject = Subject.objects.all().order_by('-name')

                if name:
                    query_subject = query_subject.filter(name__icontains=name)
                if course:
                    query_subject = query_subject.filter(course__icontains=course)
                if degree:
                    query_subject = query_subject.filter(degree__name__icontains=degree)
                if center:
                    query_subject = query_subject.filter(degree__center__name__icontains=center)
                if university:
                    query_subject = query_subject.filter(degree__center__university=university)
                if validated:
                    query_subject = query_subject.filter(validated=validated)

                context = {'subjects': query_subject, 'form': form}
                return render(request, "advanced_search_subjects.html", context)

        else:
            # query = request.GET.get("search")
            # query_subject = Subject.objects.filter(name__icontains=query)
            query_subject = Subject.objects.all().order_by('name')
            form = UserAdvancedSearchSubjectForm()
            context = {'subjects': query_subject, 'form': form}
            return render(request, "advanced_search_subjects.html", context)

    else:
        return redirect("login")


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
                rating = form.cleaned_data.get('rating')
                start_date = form.cleaned_data.get('start_date')
                end_date = form.cleaned_data.get('end_date')
                query_video = Video.objects.all().order_by('-views')

                print(user)
                if title:
                    query_video = query_video.filter(title__icontains=title).order_by('-views')
                if user:
                    query_video = query_video.filter(user__username__contains=user).order_by('-views')
                if description:
                    query_video = query_video.filter(description__icontains=description).order_by('-views')
                if likes:
                    query_video = query_video.filter(video__likes=likes).order_by('-views')
                if dislikes:
                    query_video = query_video.filter(video__dislikes=dislikes).order_by('-views')
                if views:
                    query_video = query_video.filter(views__gte=views).order_by('-views')
                if subjects:
                    query_video = query_video.filter(subjects__name__icontains=subjects).order_by('-views')
                if rating:
                    query_video = query_video.filter(content_type__overall_rating__rating__gte=rating).order_by(
                        '-views')
                print(query_video)
                context = {'videos': query_video, 'form': form}
                return render(request, "advanced_search_videos.html", context)

        else:
            # query = request.GET.get("search")
            # query_video = Video.objects.filter(title__icontains=query)
            query_video = Video.objects.all().order_by('title')
            form = UserAdvancedSearchVideoForm()
            context = {'videos': query_video, 'form': form}
            return render(request, "advanced_search_videos.html", context)

    else:
        return redirect("login")


def rating_user(request, slug):
    user = get_object_or_404(UserProfile, slug=slug)
    rating_value = request.POST.get('rating')
    # print("USER" + str(user))
    if rating_value:
        instance_rating = RatingUser.objects.get_or_create(user_rated=user, user_rating=request.user)[0]
        instance_rating.vote = rating_value
        instance_rating.save(update_fields=['vote'])
        # print("RATING: " + str(instance_rating.vote))
    return redirect(user.get_absolute_url())


def main_page(request):
    form = CommentForm(request.POST or None)
    query_list_users = None
    query_list_users_all = UserProfile.objects.all().exclude(username__icontains='admin')
    query_list_videos_all = Video.objects.all()
    query_list_comments_all = Comment.objects.all()
    query_list_subjects_all = Subject.objects.all()
    # query_list_subjects = None
    user = request.user

    comments = None
    top3users = UserProfile.objects.annotate(num_items=Count('followers')).order_by('num_items').reverse()[:3]
    top3videosviews = Video.objects.order_by('views').reverse()[:3]
    top3videoslikes = Video.objects.order_by('likes').reverse()[:3]

    if user.is_authenticated:
        user_mod = get_object_or_404(UserProfile, pk=user.pk)
        query_list_users = UserProfile.objects.filter(subjects__in=user.subjects.all()).exclude(pk=user.pk).distinct()
        comments = Comment.objects.filter(user__in=user.followers.all()).exclude(user=user)
        # query_list_subjects = Subject.objects.all()
        # print(query_list_subjects)
        content = {
            "comments": comments,
            "user_": user,
            "user": user_mod,
            'form': form,
            "users": query_list_users,
            "all_users": query_list_users_all,
            "all_subjects": query_list_subjects_all,
            "all_comments": query_list_comments_all,
            "all_videos": query_list_videos_all,
            "top3users": top3users,
            "top3videosviews": top3videosviews,
            "top3videoslikes": top3videoslikes,
        }
    else:
        content = {
            "comments": comments,
            "user_": user,
            'form': form,
            "users": query_list_users,
            "all_users": query_list_users_all,
            "all_subjects": query_list_subjects_all,
            "all_comments": query_list_comments_all,
            "all_videos": query_list_videos_all,
            "top3users": top3users,
            "top3videosviews": top3videosviews,
            "top3videoslikes": top3videoslikes,
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


class CommentDisLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        comment_id = self.kwargs.get("comment_id")
        # print(comment_id)
        comment_instance = get_object_or_404(Comment, id=comment_id)
        user = self.request.user
        url_ = user.get_absolute_url()
        if user.is_authenticated:
            if user in comment_instance.likes.all():
                comment_instance.dislikes.remove(user)
            else:
                comment_instance.dislikes.add(user)
        else:
            return "/login"
        return url_


class VideoLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        video_id = self.kwargs.get("video_id")
        # print(video_id)
        video_instance = get_object_or_404(Video, id=video_id)
        user = self.request.user
        url_ = video_instance.get_absolute_url()
        # print(url_ + "/video/" + video_id + "/")

        if user.is_authenticated:
            if user in video_instance.likes.all():
                video_instance.likes.remove(user)
            else:
                video_instance.likes.add(user)
                if user in video_instance.dislikes.all():
                    video_instance.dislikes.remove(user)
        else:
            return "/login"
        return url_


class VideoDisLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        video_id = self.kwargs.get("video_id")
        # print(video_id)
        video_instance = get_object_or_404(Video, id=video_id)
        user = self.request.user
        # url_ = "/videos/" + video_id + "/"
        url_ = video_instance.get_absolute_url()
        # print(url_ + "/video/" + video_id + "/")

        if user.is_authenticated:
            if user in video_instance.dislikes.all():
                video_instance.dislikes.remove(user)
            else:
                video_instance.dislikes.add(user)
                if user in video_instance.likes.all():
                    video_instance.likes.remove(user)
        else:
            return "/login"
        return url_


'''
class VideoRatingToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        video_id = self.kwargs.get("video_id")
        rating = self.kwargs.get("rating")

        # print(video_id)
        video_instance = get_object_or_404(Video, id=video_id)
        user = self.request.user
        url_ = video_instance.get_absolute_url()
        # print(url_ + "/video/" + video_id + "/")
        if user.is_authenticated:
            video_instance.rating = Rating.objects.create(
                user=user,
                object_id=video_instance.id,
                content_type=ContentType.objects.get_for_model(video_instance),
                content_type_id=video_instance.id,
                rating=rating,

            )
            video_instance.save()
        else:
            return "/login"
        return url_

'''


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
        title = "Iniciar sesion"
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
        title = "Registro"
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            # form.save_m2m
            new_user = authenticate(username=user.username, password=password)
            login(request, new_user)
            # if next:
            #     return redirect(next)
            return redirect("/")
    else:
        return redirect("/")
    context = {
        "form": form,
        "title": title,
    }
    return render(request, "form.html", context)


def logout_view(request):
    logout(request)
    return redirect("/")


def myvideos(request):
    user = request.user
    videos = Video.objects.filter(user=user).order_by('title')

    content = {
        'user': user,
        'videos': videos,
    }
    return render(request, 'myvideos.html', content)


def uploadVideo(request):
    if request.method == 'POST':
        user_au = request.user
        new_video = Video(
            user=user_au,
            title=request.POST['title'],
            file=request.FILES.get('file'),
        )
        new_video.save(),
        messages.success(request, "item saved")
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
