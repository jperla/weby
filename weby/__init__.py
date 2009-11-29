from __future__ import absolute_import

from .templates import template
from .templates import recursively_iterate
from . import http
from . import apps
from . import defaults
from . import email
from . import middleware
from . import tests
from . import urls

import os, time, types

def run(app, reload=False):
    http.server.serve(app, host=defaults.host, port=defaults.port, reload=reload)

def urlable_page(*args):
    def decorator(f):
        return apps.urlable(*args)(apps.page()(f))
    return decorator


def wsgify(app, *middleware_to_apply):
    return middleware.install_middleware(apps.WSGIApp(app), middleware_to_apply)

