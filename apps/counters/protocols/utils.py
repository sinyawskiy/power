# -*- coding: utf-8 -*-
import importlib
from django.utils import six


def import_attribute(path):
    assert isinstance(path, six.string_types)
    pkg, attr = path.rsplit('.', 1)
    ret = getattr(importlib.import_module(pkg), attr)
    return ret