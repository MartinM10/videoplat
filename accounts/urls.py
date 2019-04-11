from django.conf.urls import url

from .views import (
    profile_detail,
    main_page,
    CommentLikeToggle,
    FollowToggle,
    search,
    profile_edit,
    VideoLikeToggle)

app_name = 'accounts'
urlpatterns = [
    url(r'^$', main_page, name="list"),
    url(r'^search/', search, name="search"),
    url(r'^comments/(?P<comment_id>\d+)/likes/$', CommentLikeToggle.as_view(), name="like_toggle"),
    url(r'^video/(?P<video_id>\d+)/likes/$', VideoLikeToggle.as_view(), name="like_video_toggle"),

    url(r'^(?P<slug>[\w-]+)/follow/$', FollowToggle.as_view(), name="follow_toggle"),
    url(r'^(?P<slug>[\w-]+)/edit/$', profile_edit, name="edit"),

    # url(r'^(?P<slug>[\w-]+)/video/(?P<video_id>\d+)', exshow, name="video_id"),

    url(r'^(?P<slug>[\w-]+)/', profile_detail, name="detail"),

    # url(r'^(?P<slug>[\w-]+)/(?P<comment_id>\d+)/likes$', CommentLikeToggle.as_view(), name="like_toggle"),

]
