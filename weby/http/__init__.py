from __future__ import absolute_import
import logging


from ..lib import webob as _webob
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
# http://www.askapache.com/htaccess/apache-status-code-headers-errordocument.html
reason_phrases = {
    100:'Continue',
    101:'Switching Protocols',
    102:'Processing',
    200:'OK',
    201:'Created',
    202:'Accepted',
    203:'Non-Authoritative Information',
    204:'No Content',
    205:'Reset Content',
    206:'Partial Content',
    207:'Multi-Status',
    226:'IM Used',
    300:'Multiple Choices',
    301:'Moved Permanently',
    302:'Found',
    303:'See Other',
    304:'Not Modified',
    305:'Use Proxy',
    306:'Switch Proxy',
    307:'Temporary Redirect',
    400:'Bad Request',
    401:'Unauthorized',
    402:'Payment Required',
    403:'Forbidden',
    404:'Not Found',
    405:'Method Not Allowed',
    406:'Not Acceptable',
    407:'Proxy Authentication Required',
    408:'Request Time-out',
    409:'Conflict',
    410:'Gone',
    411:'Length Required',
    412:'Precondition Failed',
    413:'Request Entity Too Large',
    414:'Request-URI Too Large',
    415:'Unsupported Media Type',
    416:'Requested range not satisfiable',
    417:'Expectation Failed',
    418:'I\'m a teapot',
    422:'Unprocessable Entity',
    423:'Locked',
    424:'Failed Dependency',
    425:'Unordered Collection',
    426:'Upgrade Required',
    449:'Retry With',
    500:'Internal Server Error',
    501:'Not Implemented',
    502:'Bad Gateway',
    503:'Service Unavailable',
    504:'Gateway Time-out',
    505:'HTTP Version Not Supported',
    506:'Variant Also Negatotiates',
    507:'Insufficient Storage',
    509:'Bandwidth Limit Exceeded',
    510:'Not Extended',
}

from . import headers
from . import status

from . import defaults
from . import server
from . import types


