# -*- coding: utf-8 -*-

class ImmediateHttpResponse(Exception):
    """
    This exception is used to interrupt the flow of processing to immediately
    return a custom HttpResponse.
    """
    def __init__(self, response):
        self.response = response


class BaseAdapter(object):
    def __init__(self, request):
        self.request = request


class BaseAdapterView(object):
    @classmethod
    def adapter_view(cls, adapter):
        def view(request, *args, **kwargs):
            self = cls()
            self.request = request
            self.adapter = adapter(request)
            try:
                return self.dispatch(request, *args, **kwargs)
            except ImmediateHttpResponse as e:
                return e.response
        return view


class BaseVCPView(BaseAdapterView):
    def dispatch(self, request):
        self.protocol = self.adapter.get_protocol()


class BaseReadingsView(BaseAdapterView):
    pass