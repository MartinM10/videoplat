from django.conf import settings
from django.db import models

from accounts.models import UserProfile
from comments.models import Comment

'''
class SubjectsVideos(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    # tema = models.CharField(max_length=45, blank=True, null=True)
    # examen = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'subject_videos'
        unique_together = (('subject', 'video'),)
        ordering = ['-added']

    def __str__(self):
        return '{}' " - " '{}'.format(self.subject, self.video)
'''


class University(models.Model):
    DOMAIN = (('PU', 'Public'), ('PR', 'Private'))
    name = models.CharField(max_length=255, blank=True, null=True)
    acronym = models.CharField(max_length=5, blank=True, null=True, default='')
    website = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    domain = models.CharField(max_length=2, null=True, choices=DOMAIN)
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-added']

    def __str__(self):
        return self.name


class Center(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    rector = models.CharField(max_length=50, blank=True, null=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE)  # Field name made lowercase.
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-added']

    def __str__(self):
        return self.name


class Degree(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    credits = models.IntegerField(blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    # Relationships
    center = models.ForeignKey(Center, blank=True, null=True, on_delete=models.CASCADE)

    # subject = models.ForeignKey(Subject, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-added']

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    course = models.CharField(max_length=50, blank=True, null=True)
    validated = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    topic = models.PositiveSmallIntegerField(blank=True, null=True)
    # Relationships
    degree = models.ForeignKey(Degree, blank=True, null=True, on_delete=models.CASCADE)

    # video = models.ManyToManyField(Video, blank=True,
    # related_name="subject_videos")

    class Meta:
        ordering = ['-added']
        unique_together = (('name', 'degree', 'topic'),)

    def __str__(self):
        cadena = self.name + " || " + self.course + "|| " + self.degree.name + " || (" + self.degree.center.university.acronym + ")"
        return cadena


# class CentersDegrees(models.Model):
#     center = models.ForeignKey(Center, on_delete=models.CASCADE)
#     degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
#     added = models.DateTimeField(auto_now_add=True)
#     edited = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         db_table = 'centers_degrees'
#         unique_together = (('center', 'degree'),)
#         ordering = ['-added']
#
#     def __str__(self):
#         return '{}' " - " '{}'.format(self.center, self.degree)

'''
class DegreesSubjects(models.Model):
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=50, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('degree', 'subject'),)

    def __str__(self):
        return '{}' " - " '{}'.format(self.degree, self.subject)
'''

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

    # propietario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, db_column='propietario')  # Field name made lowercase.

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

# class UsersSubjects(models.Model):
#     user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     added = models.DateTimeField(auto_now_add=True)
#     edited = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         unique_together = (('user', 'subject'),)
#         ordering = ['-added']
#
#     def __str__(self):
#         return '{}' " - " '{}'.format(self.user, self.subject)
