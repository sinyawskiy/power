# -*- coding: utf-8 -*-
import importlib
from collections import OrderedDict
from django.conf import settings


class ProtocolRegistry(object):
    def __init__(self):
        self.protocol_map = OrderedDict()
        self.loaded = False

    def get_list(self, request=None):
        self.load()
        return [
            protocol_cls(request)
            for protocol_cls in self.protocol_map.values()]

    def register(self, cls):
        self.protocol_map[cls.id] = cls

    def by_id(self, id, request=None):
        self.load()
        return self.protocol_map[id](request=request)

    def as_choices(self):
        self.load()
        for protocol_cls in self.protocol_map.values():
            yield (protocol_cls.id, protocol_cls.name)

    def load(self):
        # TODO: Providers register with the provider registry when
        # loaded. Here, we build the URLs for all registered providers. So, we
        # really need to be sure all providers did register, which is why we're
        # forcefully importing the `provider` modules here. The overall
        # mechanism is way to magical and depends on the import order et al, so
        # all of this really needs to be revisited.
        if not self.loaded:
            for app in settings.INSTALLED_APPS:
                try:
                    protocol_module = importlib.import_module(
                        app + '.protocol'
                    )
                except ImportError:
                    pass
                else:
                    for cls in getattr(
                        protocol_module, 'protocol_classes', []
                    ):
                        self.register(cls)
            self.loaded = True


registry = ProtocolRegistry()