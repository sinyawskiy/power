# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..addresses.models import Address
from . import protocols


class Vendor(models.Model):
    title = models.CharField(u'наименование', max_length=255)

    def __unicode__(self):
        return u'%s' % self.title

    class Meta:
        verbose_name = u'производитель'
        verbose_name_plural = u'производители'


class EquipmentModel(models.Model):
    vendor = models.ForeignKey(Vendor, verbose_name=u'производитель')
    title = models.CharField(u'наименование', max_length=255)

    def __unicode__(self):
        return u'%s %s' % (self.vendor, self.title)

    class Meta:
        verbose_name = u'модель'
        verbose_name_plural = u'модели'


class Counter(models.Model):
    equipment = models.ForeignKey(EquipmentModel, verbose_name=u'счётчик')
    address = models.ForeignKey(Address, verbose_name=u'адрес', blank=True, null=True)
    host = models.CharField(u'IP адрес', max_length=255)
    port = models.IntegerField(u'порт')
    timeout = models.IntegerField(u'таймаут сек.')
    serial = models.CharField(u'серийный номер', max_length=255)
    phone = models.CharField(u'номер телефона', max_length=255)
    sim = models.CharField(u'номер SIM карты', max_length=255)
    protocol = models.CharField(verbose_name=u'протокол', max_length=30, choices=protocols.registry.as_choices())

    def __unicode__(self):
        return u'%s' % self.equipment

    class Meta:
        verbose_name = u'счётчик'
        verbose_name_plural = u'счётчики'