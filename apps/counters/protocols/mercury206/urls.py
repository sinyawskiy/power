# -*- coding: utf-8 -*-
from ..urls import default_urlpatterns
from .protocol import Mercury206Protocol


urlpatterns = default_urlpatterns(Mercury206Protocol)
