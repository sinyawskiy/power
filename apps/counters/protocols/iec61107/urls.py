# -*- coding: utf-8 -*-
from ..urls import default_urlpatterns
from .protocol import IEC61107Protocol


urlpatterns = default_urlpatterns(IEC61107Protocol)
