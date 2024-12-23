import os
from django.conf import settings


class _Null(object):
    pass


Null = _Null()


def get(key, default, aliases=None):
    """从`djang.conf.settings`中或环境变量中获取配置。
    """
    aliases = aliases or []
    value = getattr(settings, key, Null)
    if value is Null:
        value = os.environ.get(key, Null)
    for alias in aliases:
        if value is Null:
            value = getattr(settings, alias, Null)
        if value is Null:
            value = os.environ.get(alias, Null)
    if value is Null:
        value = default
    return value
