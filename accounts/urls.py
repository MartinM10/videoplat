from django.conf.urls import url

from .views import (
    profile_detail,
    main_page,
    CommentLikeToggle,
    FollowToggle,
    search,
    profile_edit,
    VideoLikeToggle, VideoDisLikeToggle, CommentDisLikeToggle, advanced_search_users, advanced_search_subjects,
    advanced_search_videos)

app_name = 'accounts'
urlpatterns = [
    url(r'^$', main_page, name="list"),
    url(r'^search/$', search, name="search"),
    url(r'^search/advanced_search_users/$', advanced_search_users, name="advanced_search_users"),
    url(r'^search/advanced_search_subjects/$', advanced_search_subjects, name="advanced_search_subjects"),
    url(r'^search/advanced_search_videos/$', advanced_search_videos, name="advanced_search_videos"),

    url(r'^comments/(?P<comment_id>\d+)/likes/$', CommentLikeToggle.as_view(), name="like_toggle"),
    url(r'^comments/(?P<comment_id>\d+)/dislikes/$', CommentDisLikeToggle.as_view(), name="dislike_toggle"),

    url(r'^video/(?P<video_id>\d+)/likes/$', VideoLikeToggle.as_view(), name="like_video_toggle"),
    url(r'^video/(?P<video_id>\d+)/dislikes/$', VideoDisLikeToggle.as_view(), name="dislike_video_toggle"),

    # url(r'^video/(?P<video_id>\d+)/rating/$', VideoRatingToggle.as_view(), name="rating_video_toggle"),

    url(r'^(?P<slug>[\w-]+)/follow/$', FollowToggle.as_view(), name="follow_toggle"),
    url(r'^(?P<slug>[\w-]+)/edit/$', profile_edit, name="edit"),

    # url(r'^(?P<slug>[\w-]+)/video/(?P<video_id>\d+)', exshow, name="video_id"),

    url(r'^(?P<slug>[\w-]+)/', profile_detail, name="detail"),

    # url(r'^(?P<slug>[\w-]+)/(?P<comment_id>\d+)/likes$', CommentLikeToggle.as_view(), name="like_toggle"),

]
