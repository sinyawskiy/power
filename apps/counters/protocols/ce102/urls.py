# -*- coding: utf-8 -*-
from ..urls import default_urlpatterns
from .protocol import CE102Protocol


urlpatterns = default_urlpatterns(CE102Protocol)
