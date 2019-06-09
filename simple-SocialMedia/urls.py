"""DailyStory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import main_page, about, register_view, login_view, logout_view, uploadVideo, list_subjects, \
    myvideos

# exshow

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^about/', about, name='about'),
    url(r'^login/', login_view, name='login'),
    url(r'^register/', register_view, name='register'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^videos/', include('videos.urls')),
    url(r'^myvideos/', myvideos, name='myvideos'),

    url(r'^videoupload/', uploadVideo, name='videoupload'),

    url(r'^subjects/', include('subjects.urls')),

    # url(r'^show/(\S+)/(\S+)/$', exshow),
    # url(r"^ratings/", include("pinax.ratings.urls", namespace="pinax_ratings")),

    # url(r'^ratings/', include('star_ratings.urls', namespace='ratings')),

    url(r'^$', main_page, name='main'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
