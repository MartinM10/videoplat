# this page from try-django 1.9 course not from me
from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.forms import SelectDateWidget

from subjects.models import Subject, University
from videos.models import Video
from .models import UserProfile

COURSE_CHOICES = (
    ('', ''),
    ('1º', '1º'),
    ('2º', '2º'),
    ('3º', '3º'),
    ('4º', '4º'),
)


class UserProfileForm(forms.ModelForm):
    """docstring for PostForm """

    class Meta:
        """docstring for Meta"""
        model = UserProfile
        fields = [
            "slug",
            "first_name",
            "last_name",
            # "interests",
            "image",
        ]


# User = get_user_model() NO ESTOY SEGURO
User = UserProfile


class UserAdvancedSearchUserForm(forms.Form):
    username = forms.CharField(label="username", required=False)
    first_name = forms.CharField(label="first_name", required=False)
    last_name = forms.CharField(label="last_name", required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
        ]


class UserAdvancedSearchSubjectForm(forms.Form):
    name = forms.CharField(label="name", required=False)
    course = forms.ChoiceField(choices=COURSE_CHOICES, label="course", required=False)
    degree = forms.CharField(label="degree", required=False)
    center = forms.CharField(label="center", required=False)
    university = forms.ModelChoiceField(queryset=University.objects.all(), empty_label="", required=False)

    class Meta:
        model = Subject
        fields = [
            'name',
            'course',
            'degree',
            'center',
            'university',
        ]


class UserAdvancedSearchVideoForm(forms.Form):
    title = forms.CharField(label="Título", required=False)
    user = forms.CharField(label="Propietario", required=False)
    description = forms.CharField(label="Descripcion", required=False)
    likes = forms.IntegerField(label="Nº de Likes", required=False)
    dislikes = forms.IntegerField(label="Nº de Dislikes", required=False)
    views = forms.IntegerField(label="Visualizaciones", required=False)
    subjects = forms.CharField(label="Asignatura", required=False)
    start_date = forms.DateField(
        widget=SelectDateWidget(
            empty_label=("Año", "Mes", "Día")
        ), required=False, label="Fecha Inicio"
    )
    end_date = forms.DateField(
        widget=SelectDateWidget(
            empty_label=("Año", "Mes", "Día"),
        ), required=False, label="Fecha Fin"
    )

    class Meta:
        model = Video
        fields = [
            'title',
            'user',
            'description',
            'likes',
            'dislikes',
            'views',
            'subjects',
            'start_date'
            'end_date'
        ]

    class Meta:
        model = Video
        fields = [
            'title',
            'user',
            'description',
            'likes',
            'dislikes',
            'views',
            'subject',
            'start_date',
            'end_date'
        ]


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        # user_qs = User.objects.filter(username=username)
        # if user_qs.count() == 1:
        #     user = user_qs.first()
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect passsword")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label="username")
    email = forms.EmailField(label='Email address')
    email2 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        # if (i.isupper() for i in username):
        # raise forms.ValidationError("username should be lowercase without white spaces")
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError("Emails must match")
        email_qs = User.objects.filter(email=email)
        username_qs = User.objects.filter(username=username)
        if email_qs.exists() or username_qs.exists():
            raise forms.ValidationError("This email or username has already been registered")

        return super(UserRegisterForm, self).clean(*args, **kwargs)
