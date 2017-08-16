# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from .utils import import_attribute


def default_urlpatterns(protocol):
    vcp_view = import_attribute(
        protocol.get_package() + '.views.vcp_view')
    readings_view = import_attribute(
        protocol.get_package() + '.views.readings_view')

    urlpatterns = [
        url(r'^vcp/$',
            vcp_view, name=protocol.id + "_vcp"),
        url(r'^readings/$',
            readings_view, name=protocol.id + "_readings"),
    ]

    return [url('^' + protocol.get_slug() + '/', include(urlpatterns))]