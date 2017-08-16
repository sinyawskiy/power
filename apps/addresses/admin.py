# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import CityArea, Address


class CityAreaAdmin(admin.ModelAdmin):
    model = CityArea
    list_display = ('__unicode__',)

admin.site.register(CityArea, CityAreaAdmin)
admin.site.register(Address)