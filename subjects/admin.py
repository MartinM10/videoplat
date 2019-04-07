# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from subjects.models import Subject


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


admin.site.register(Subject, SubjectAdmin)
