# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from subjects.models import Subject, Degree, University, Center


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


admin.site.register(Subject, SubjectAdmin)


class DegreeAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


admin.site.register(Degree, DegreeAdmin)


class UniversityAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


admin.site.register(University, UniversityAdmin)


class CenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


admin.site.register(Center, CenterAdmin)
