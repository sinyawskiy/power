# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Vendor, EquipmentModel, Counter


class CounterAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'address', 'serial', 'protocol', 'host', 'port', 'timeout', 'phone', 'sim')
    list_filter = ('address__city_area', 'equipment')

admin.site.register(Vendor)
admin.site.register(EquipmentModel)
admin.site.register(Counter, CounterAdmin)