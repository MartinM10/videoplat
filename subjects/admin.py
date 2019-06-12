# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from subjects.models import Subject, Degree, University, Center


class SubjectAdmin(ImportExportModelAdmin):
    list_display = ['name', 'id']


admin.site.register(Subject, SubjectAdmin)


class DegreeAdmin(ImportExportModelAdmin):
    list_display = ['name', 'id']


admin.site.register(Degree, DegreeAdmin)


class UniversityAdmin(ImportExportModelAdmin):
    list_display = ['name', 'id']


admin.site.register(University, UniversityAdmin)


class CenterAdmin(ImportExportModelAdmin):
    list_display = ['name', 'id']


admin.site.register(Center, CenterAdmin)
