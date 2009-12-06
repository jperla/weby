from __future__ import absolute_import

from . import apps as _apps
from . import http
'''
from . import defaults
from . import email
from . import middleware
from . import tests
from . import urls as _urls
'''

App = _apps.dispatch.SimpleDispatchApp
