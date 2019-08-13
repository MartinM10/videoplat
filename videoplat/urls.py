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
