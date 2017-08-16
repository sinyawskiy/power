# -*- coding: utf-8 -*-
from ..base import BaseTCPConnect, BaseProtocol


class Mercury206Connect(BaseTCPConnect):
    pass


class Mercury206Protocol(BaseProtocol):
    id = 'mercury206'
    name = 'Mercury 206'

    connect_class = Mercury206Connect

    def get_vcp(self):
        return 0

    def get_readings(self):
        return 0


protocol_classes = [Mercury206Protocol]