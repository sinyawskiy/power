# -*- coding: utf-8 -*-
from ..views import BaseAdapter, BaseVCPView, BaseReadingsView


class CE102Adapter(BaseAdapter):
    pass


vcp_view = BaseVCPView.adapter_view(CE102Adapter)
readings_view = BaseReadingsView.adapter_view(CE102Adapter)