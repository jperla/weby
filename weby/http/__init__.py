from __future__ import absolute_import
import logging


import webob as _webob
#Request = _webob.Request
Response = _webob.Response
# jperla: override to do chardet on all incoming data
class Request(_webob.Request):
    def get(*args, **kwargs):
        returned = _webob.Request.get(*args, **kwargs)
        if isinstance(returned, unicode):
            raise Exception(u'String already unicode: %s' % returned)
        else:
            #TODO: jperla: do chardet here
            return returned.decode(u'utf-8')

from . import headers
from . import status

from . import defaults
from . import server


