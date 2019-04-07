from django.conf.urls import url

from .views import (
    subject_detail, subject_list)

app_name = 'subjects'
urlpatterns = [
    url(r'^$', subject_list, name="subjects_list"),
    # url(r'^search/', search, name="search"),
    # url(r'^comments/(?P<comment_id>\d+)/likes/$', CommentLikeToggle.as_view(), name="like_toggle"),
    # url(r'^(?P<slug>[\w-]+)/follow/$', FollowToggle.as_view(), name="follow_toggle"),
    # url(r'^(?P<slug>[\w-]+)/edit/$', profile_edit, name="edit"),
    url(r'^(?P<name>[\w-]+)/', subject_detail, name="subject_detail"),
    # url(r'^(?P<slug>[\w-]+)/(?P<comment_id>\d+)/likes$', CommentLikeToggle.as_view(), name="like_toggle"),

]
