from __future__ import absolute_import

from webob import exc as _exc

ok = '200 OK'

HTTPController = _exc.HTTPException
HTTP301Controller = _exc.HTTPFound
HTTP404Controller = _exc.HTTPNotFound

def redirect(location, *args, **kwargs):
    raise HTTP301Controller(location=location)

def not_found(body=''):
    raise HTTP404Controller()
