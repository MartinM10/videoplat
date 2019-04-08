from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
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


class UserProfileManager(BaseUserManager):
    def create(self, username, password, **extra_fields):
        return self.create_user(username, password, **extra_fields)

    def create_user(self, username, password, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(username, password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    slug = models.SlugField(unique=True, null=True)
    username = models.CharField(unique=True, max_length=140)
    first_name = models.CharField(blank=True, max_length=140)
    last_name = models.CharField(blank=True, max_length=140)
    email = models.EmailField(blank=True, null=True)
    #interests = models.CharField(max_length=140, default="")
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
    subjects = models.ManyToManyField('subjects.Subject', blank=True, related_name="users")
    USERNAME_FIELD = 'username'
    objects = UserProfileManager()
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.username

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
    slug = slugify(instance.username)
    if new_slug is not None:
        slug = new_slug
    qs = UserProfile.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug)
    return slug


def create_profile(sender, instance, **kwargs):
    instance.slug = create_slug(instance)


pre_save.connect(create_profile, sender=UserProfile)
