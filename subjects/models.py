from django.conf import settings
from django.db import models

from accounts.models import UserProfile
from comments.models import Comment


class Subject(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    validated = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    #video = models.ManyToManyField(Video, blank=True,
    # related_name="subject_videos")

    class Meta:
        db_table = 'subject'
        ordering = ['-added']

    def __str__(self):
        return self.name


'''
class SubjectsVideos(models.Model):
    subject = models.ForeignKey(Subject, models.CASCADE)
    video = models.ForeignKey(Video, models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    # tema = models.CharField(max_length=45, blank=True, null=True)
    # examen = models.CharField(max_length=45, blank=True, null=True)
'''


class Meta:
    db_table = 'subject_videos'
    unique_together = (('subject', 'video'),)
    ordering = ['-added']


def __str__(self):
    return '{}' " - " '{}'.format(self.subject, self.video)


class University(models.Model):
    DOMAIN = (('PU', 'Public'), ('PR', 'Private'))
    name = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    domain = models.CharField(max_length=2, null=True, choices=DOMAIN)
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'university'
        ordering = ['-added']

    def __str__(self):
        return self.name


class Center(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    rector = models.CharField(max_length=50, blank=True, null=True)
    university = models.ForeignKey(University, models.CASCADE)  # Field name made lowercase.
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'center'
        ordering = ['-added']

    def __str__(self):
        return self.nombre


class Degree(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    credits = models.IntegerField(blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'degree'
        ordering = ['-added']

    def __str__(self):
        return self.name


class CentersDegrees(models.Model):
    center = models.ForeignKey(Center, models.CASCADE)
    degree = models.ForeignKey(Degree, models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'centers_degrees'
        unique_together = (('center', 'degree'),)
        ordering = ['-added']

    def __str__(self):
        return '{}' " - " '{}'.format(self.center, self.degree)


class DegreesSubjects(models.Model):
    degree = models.ForeignKey(Degree, models.CASCADE)
    subject = models.ForeignKey(Subject, models.CASCADE)
    academic_year = models.CharField(max_length=50, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'degrees_subjects'
        unique_together = (('degree', 'subject'),)
        ordering = ['-added']

    def __str__(self):
        return '{}' " - " '{}'.format(self.degree, self.subject)


'''
class Video(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    duracion = models.IntegerField(blank=True, null=True)
    visualizaciones = models.BigIntegerField(blank=True, null=True)
    puntuacion = models.IntegerField(blank=True, null=True)
    subido = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    # propietario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='propietario')  # Field name made lowercase.

    class Meta:
        db_table = 'video'

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    fecha_nacimiento = models.DateField(blank=True, null=True)
    puntuacion = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.username
'''


class UsersSubjects(models.Model):
    user = models.ForeignKey(UserProfile, models.CASCADE)
    subject = models.ForeignKey(Subject, models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users_subjects'
        unique_together = (('user', 'subject'),)
        ordering = ['-added']

    def __str__(self):
        return '{}' " - " '{}'.format(self.user, self.subject)
