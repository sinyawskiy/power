# -*- coding: utf-8 -*-
from ..views import BaseAdapter, BaseVCPView, BaseReadingsView


class IEC61107Adapter(BaseAdapter):
    pass


vcp_view = BaseVCPView.adapter_view(IEC61107Adapter)
readings_view = BaseReadingsView.adapter_view(IEC61107Adapter)