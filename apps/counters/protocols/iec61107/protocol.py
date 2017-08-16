# -*- coding: utf-8 -*-
from ..base import BaseTCPConnect, BaseProtocol


class IEC61107Connect(BaseTCPConnect):
    pass


class IEC61107Protocol(BaseProtocol):
    id = 'iec61107'
    name = 'IEC 61107'

    connect_class = IEC61107Connect

    def get_vcp(self):
        return 0

    def get_readings(self):
        return 0


protocol_classes = [IEC61107Protocol]