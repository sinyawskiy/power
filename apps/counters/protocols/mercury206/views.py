# -*- coding: utf-8 -*-
from ..views import BaseAdapter, BaseVCPView, BaseReadingsView


class Mercury206Adapter(BaseAdapter):
    pass


vcp_view = BaseVCPView.adapter_view(Mercury206Adapter)
readings_view = BaseReadingsView.adapter_view(Mercury206Adapter)