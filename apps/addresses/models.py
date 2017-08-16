# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class CityArea(models.Model):
    name = models.CharField(u'наименование района', max_length=255)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = u'район'
        verbose_name_plural = u'районы'


class Address(models.Model):
    city_area = models.ForeignKey(CityArea, verbose_name=u'район', null=True, blank=True)
    longitude = models.FloatField(u'Долгота', null=True, blank=True)
    latitude = models.FloatField(u'Широта', null=True, blank=True)
    address = models.CharField(u'адрес', max_length=255)
    description = models.TextField(u'описание', blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.address

    class Meta:
        verbose_name = u'адрес'
        verbose_name_plural = u'адреса объектов'