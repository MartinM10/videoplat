from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.urls import reverse


# Create your models here.
def upload_location(instance, filename):
    # filebase, extension = filename.split('.')
    # return "%s/%s.%s%(instance.id, filebase, extension)
    return "%s/%s" % (instance.id, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first = models.CharField(max_length=100, default="")
    last = models.CharField(max_length=100, default="")

    interests = models.CharField(max_length=140, default="")

    slug = models.SlugField(unique=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    image = models.ImageField(
        upload_to=upload_location,
        null=True, blank=True,
        height_field='height_field',
        width_field='width_field',
    )
    height_field = models.IntegerField(default=0, null=True, blank=True)
    width_field = models.IntegerField(default=0, null=True, blank=True)

    followers = models.ManyToManyField('self', blank=True, related_name="followers")
    subjects = models.ManyToManyField('subjects.Subject', null=True, related_name="users")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("accounts:detail", kwargs={"slug": self.slug})

    def get_follow_instances(self):
        return self.followers.all()

    def get_follow_url(self):
        return reverse("accounts:follow_toggle", kwargs={"slug": self.slug})

    @property
    def get_instance_centent_type(self):
        return ContentType.objects.get_for_model(self.__class__)


def create_slug(instance, new_slug=None):
    slug = slugify(instance.user.username)
    if new_slug is not None:
        slug = new_slug
    qs = UserProfile.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug)
    return slug


def create_profile(sender, instance, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=instance)
        user_profile.slug = create_slug(user_profile)
        user_profile.save()
        print(user_profile.slug)


post_save.connect(create_profile, sender=User)
