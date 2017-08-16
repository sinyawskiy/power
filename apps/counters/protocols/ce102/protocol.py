# -*- coding: utf-8 -*-
from ..base import BaseTCPConnect, BaseProtocol


class CE102Connect(BaseTCPConnect):
    pass


class CE102Protocol(BaseProtocol):
    id = 'ce206'
    name = 'Energomera CE 206'

    connect_class = CE102Connect

    def get_vcp(self):
        return 0

    def get_readings(self):
        return 0


protocol_classes = [CE102Protocol]