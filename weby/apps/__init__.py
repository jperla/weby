from __future__ import absolute_import
import chardet

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
        status, headers = defaults.status_and_headers
        self.status, self.headers = status, headers

    def __call__(self, x):
        self.print_response(x)

    def print_response(self, x):
        self.__response.append(x)
    
    def redirect(self, url, type=302):
        assert type == 301 or type == 302, 'Redirect must be 301 or 302'
        self.status = '%s %s' % (type, headers.reason_phrases[type])
        self.headers += ('Location', url)

    def response(self):
        yield self.status, self.headers
        #TODO: jperla: serious work needed here
        if self.headers[0] == headers.content_types.html_utf8:
            #TODO: jperla: make this yielding and working
            for x in output_encoding(recursively_iterate(self.__response), 'utf8'):
                yield x
        else:
            #TODO: jperla: make this yielding and working
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
        req = Request(environ)
        try:
            resp = self.app(req)
            status, headers = resp.next()
        except status.HTTPController, exception:
            resp = exception
            return resp(environ, start_response)
        else:
            start_response(status, headers)
            return list(resp)

class SettingsApp(WebyApp):
    def __init__(self, settings, f):
        WebyApp.__init__(self)
        self._settings = settings
        self._f = f
    def __call__(self, req):
        req.settings = self._settings
        return self._f(req)
    def url(self):
        url = u'/'
        return self.parent.wrap_url(self, url)

class UrlableApp(WebyApp):
    def __init__(self, f, parsers):
        WebyApp.__init__(self)
        self._f = f
        self._parsers = parsers
    def __call__(self, req):
        args = []
        #TODO: jperla: assumes utf-8
        url = u'%s' % req.path_info.decode('utf-8')
        #TODO: jperla: wrongly?
        for parser in self._parsers:
            new_args, url = parser.parse(req, url)
            args.extend(new_args)
        return self._f(req, *args)
    def url(self, *args):
        url = u'/'
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

#TODO: jperla: 'as' this
from ..http import defaults, headers, Request, status
from . import dispatch
from . import standard

