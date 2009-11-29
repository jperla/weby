from __future__ import absolute_import

from .. import http
from ..templates import recursively_iterate


class WebyApp(object):
    def __init__(self):
        self.parent = None

    def __call__(self, req):
        raise NotImplementedError

    def wrap_parent(f):
        #TODO: jperla: use this everywhere somehow
        def decorator(self, subapp, suburl):
            if self.parent is None:
                return suburl
            else:
                return self.parent.wrap_url(self, suburl)
        return decorator

    @wrap_parent
    def wrap_url(self, subapp, suburl):
        return suburl

class WebyPage(object):
    def __init__(self):
        self.__response = []
        status, headers = http.defaults.status_and_headers
        self.status, self.headers = status, headers

    def __call__(self, x):
        self.print_response(x)

    def print_response(self, x):
        self.__response.append(x)

    def response(self):
        yield self.status, self.headers
        #TODO: jperla: serious work needed here
        if self.headers[0] == http.headers.content_types.html_utf8:
            for x in output_encoding(recursively_iterate(self.__response), 'utf8'):
                yield x
        else:
            for x in self.__response.append(x):
                yield x

def page():
    def decorator(f):
        def new_f(*args, **kwargs):
            page = WebyPage()
            #TODO: jperla: assumes args[0] is a request
            f(args[0], page, *args[1:], **kwargs)
            return page.response()
        return new_f
    return decorator


class WSGIApp(object):
    def __init__(self, app):
        assert(isinstance(app, WebyApp))
        self.app = app

    def __call__(self, environ, start_response):
        req = http.Request(environ)
        try:
            resp = self.app(req)
            status, headers = resp.next()
        except http.status.HTTPController, exception:
            resp = exception
            return resp(environ, start_response)
        else:
            start_response(status, headers)
            return resp

class UrlableApp(WebyApp):
    def __init__(self, f, parsers):
        WebyApp.__init__(self)
        self._f = f
        self._parsers = parsers
    def __call__(self, req):
        args = []
        url = req.path_info
        for parser in self._parsers:
            new_args, url = parser.parse(req, url)
            args.extend(new_args)
        return self._f(req, *args)
    def url(self, *args):
        url = '/'
        for parser in self._parsers:
            args, url = parser.generate(args, url)
        return self.parent.wrap_url(self, url)

def urlable(*parsers):
    def decorator(f):
        return UrlableApp(f, parsers)
    return decorator

def output_encoding(strings, encoding):
    for s in strings:
        encoded = s.encode(encoding)
        yield encoded

from . import dispatch

