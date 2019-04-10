from django.conf.urls import url

# from .views import (
#     subject_detail, subject_list)
from videos.views import showVideo

app_name = 'videos'
urlpatterns = [
    url(r'^(?P<video_id>[\d]+)/$', showVideo, name="video_id"),

]
