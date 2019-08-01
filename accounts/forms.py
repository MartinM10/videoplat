# this page from try-django 1.9 course not from me
from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.forms import SelectDateWidget

from subjects.models import Subject, University, Center, Degree
from videos.models import Video
from .models import UserProfile

COURSE_CHOICES = (
    ('', ''),
    ('1º', '1º'),
    ('2º', '2º'),
    ('3º', '3º'),
    ('4º', '4º'),
)

VALIDATED_CHOICES = (
    ('', ''),
    ('True', 'True'),
    ('False', 'False'),
)


class UserProfileForm(forms.ModelForm):
    """docstring for PostForm """
    username = forms.CharField(label="Nombre de usuario", required=False)
    first_name = forms.CharField(label="Nombre", required=False)
    last_name = forms.CharField(label="Apellido", required=False)
    email = forms.CharField(label="Email", required=False)

    subjects = forms.ModelMultipleChoiceField(label="Asignaturas de interes", widget=forms.SelectMultiple,
                                              queryset=Subject.objects.all(), required=False)

    class Meta:
        """docstring for Meta"""
        model = UserProfile
        fields = [
            "username",
            "first_name",
            "last_name",
            'email',
            # "interests",
            'subjects',
            "image",
        ]


User = UserProfile


class UserAdvancedSearchUserForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario", required=False)
    first_name = forms.CharField(label="Nombre", required=False)
    last_name = forms.CharField(label="Apellido", required=False)
    email = forms.CharField(label="Email", required=False)
    followers = forms.IntegerField(label="Nº de seguidores (>=)", required=False)

    class Meta:
        model = UserProfile
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'followers',
        ]


class UserAdvancedSearchSubjectForm(forms.Form):
    name = forms.CharField(label="Nombre", required=False)
    course = forms.ChoiceField(choices=COURSE_CHOICES, label="Curso", required=False)
    degree = forms.ModelChoiceField(queryset=Degree.objects.all().order_by('-name'), label="Grado", empty_label="",
                                    required=False)
    center = forms.ModelChoiceField(queryset=Center.objects.all().order_by('-name'), label="Centro", empty_label="",
                                    required=False)
    university = forms.ModelChoiceField(queryset=University.objects.all().order_by('-name'), label="Universidad",
                                        empty_label="",
                                        required=False)
    validated = forms.ChoiceField(choices=VALIDATED_CHOICES, label="Validada", required=False)

    class Meta:
        model = Subject
        fields = [
            'name',
            'course',
            'degree',
            'center',
            'university',
            'validated',
        ]


class UserAdvancedSearchVideoForm(forms.Form):
    title = forms.CharField(label="Título", required=False)
    user = forms.CharField(label="Propietario", required=False)
    subjects = forms.ModelChoiceField(queryset=Subject.objects.all().order_by('-name'), empty_label="", required=False)
    views = forms.IntegerField(label="Nº de Visualizaciones (>=)", required=False)
    likes = forms.IntegerField(label="Nº de Likes (>=)", required=False)
    dislikes = forms.IntegerField(label="Nº de Dislikes (>=)", required=False)
    description = forms.CharField(label="Descripcion", required=False)
    rating = forms.IntegerField(label="Rating (>=)", required=False)
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
            'rating',
            'start_date',
            'end_date',
        ]


class UserDisplayForm(forms.ModelForm):
    last_login = forms.DateField(
        widget=forms.TimeInput(format='%d/%m/%Y - %H:%M',
                               attrs={'class': 'form-control',
                                      'readonly': 'readonly'}), required=False, label='Ultimo acceso')
    added = forms.DateField(
        widget=forms.TimeInput(format='%d/%m/%Y - %H:%M',
                               attrs={'class': 'form-control', 'readonly': 'readonly'}), required=False)

    class Meta:
        model = UserProfile
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'last_login',
        ]
        labels = {
            'username': 'Username',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Email',
            'last_login': 'Ultimo acceso',
            'added': 'Registro',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'added': forms.DateField(
                widget=forms.TimeInput(format='%d/%m/%Y - %H:%M',
                                       attrs={'class': 'form-control', 'readonly': 'readonly'}), required=False)
        }


class UserLoginForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        # user_qs = User.objects.filter(username=username)
        # if user_qs.count() == 1:
        #     user = user_qs.first()
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Este usuario no existe")
            if not user.check_password(password):
                raise forms.ValidationError("Contraseña incorrecta")
            if not user.is_active:
                raise forms.ValidationError("Este usuario ya no está activo.")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label="Nombre de usuario")
    email = forms.EmailField(label='Email')
    email2 = forms.EmailField(label='Confirmar Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

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
            raise forms.ValidationError("El email debe coincidir")
        email_qs = User.objects.filter(email=email)
        username_qs = User.objects.filter(username=username)
        if email_qs.exists() or username_qs.exists():
            raise forms.ValidationError("Este email ya está registrado")

        return super(UserRegisterForm, self).clean(*args, **kwargs)
