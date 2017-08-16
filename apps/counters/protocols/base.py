# -*- coding: utf-8 -*-


class AuthProcess(object):
    LOGIN = 'login'
    CONNECT = 'connect'
    REDIRECT = 'redirect'


class AuthAction(object):
    AUTHENTICATE = 'authenticate'
    REAUTHENTICATE = 'reauthenticate'


class AuthError(object):
    UNKNOWN = 'unknown'
    CANCELLED = 'cancelled'  # Cancelled on request of user
    DENIED = 'denied'  # Denied by server


class ProtocolException(Exception):
    pass


class BaseProtocol(object):
    slug = None

    @classmethod
    def get_slug(cls):
        return cls.slug or cls.id


class BaseTCPConnect(object):
    def __init__(self, counter):
        self.counter = counter
