from __future__ import absolute_import

import sys
import urllib
import urlparse
import StringIO

import webob

import tornado.httpserver
import tornado.ioloop
import tornado.web

from ...http import reason_phrases

def wrap_tornado(app):
    def new(tornado_request):
        #TODO: jperla: wrap into complete wsgi-like request
        args = '&'.join('%s=%s' % (urllib.quote(k),urllib.quote(v[0])) for k,v in tornado_request.arguments.iteritems())
        req = webob_request_from_tornado_request(tornado_request)
        body = app(req)
        status, headers = body.next()
        #TODO: jperla: make this return 404 appropriately
        status_line = 'HTTP/1.1 %s\r\n' % status
        headers = ''.join(['%s: %s\r\n' % h for h in headers])
        content = ''.join(body)
        content_length = 'Content-Length: %d\r\n' % len(content)
        tornado_request.write(status_line + content_length + headers + '\r\n')
        tornado_request.write(content);
        #for b in body:
        #    tornado_request.write(b)
        #TODO: jperla: make this iterate?
        tornado_request.finish()
    return new

def webob_request_from_tornado_request(tornado_request):
    #return webob.Request.blank(tornado_request.uri)
    return webob.Request(wsgi_environ_from_tornado_request(tornado_request))


def wsgi_environ_from_tornado_request(tornado_request):
    '''
    http://www.python.org/dev/peps/pep-0333/#environ-variables
    '''
    environ = {}
    environ['REQUEST_METHOD'] = tornado_request.method
    environ['SCRIPT_NAME'] = ''
    environ['PATH_INFO'] = tornado_request.path
    environ['QUERY_STRING'] = tornado_request.query
    scheme, netloc, path, query, fragment = urlparse.urlsplit(tornado_request.uri)
    server_name, server_port = netloc.split(':', 1) if (':' in netloc) else netloc, '80'
    environ['SERVER_NAME'] = server_name
    environ['SERVER_PORT'] = int(server_port)
    environ['SERVER_PROTOCOL'] = tornado_request.version
    environ['wsgi.version'] = (1, 0)
    environ['wsgi.url_scheme'] = scheme
    environ['wsgi.input'] = StringIO.StringIO(tornado_request.body)
    environ['wsgi.errors'] = sys.stderr
    environ['wsgi.multithread'] = True
    environ['wsgi.multiprocess'] = True
    environ['wsgi.run_once'] = False
    for h,v in tornado_request.headers.iteritems():
        environ['HTTP_%s' % h.upper().replace('-', '_')] = v
    #TODO: jperla: put in content type and length for file uploads ?
    return environ

def start(app, host=None, port=8088):
    assert not isinstance(app, WSGIApp), 'Tornado server does not support WSGIApps'
    assert isinstance(app, WebyApp), 'Tornado server wrapper supports WebyApps'
    tornado_app = wrap_tornado(app)
    http_server = tornado.httpserver.HTTPServer(tornado_app)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

serve = start

from ...apps import WSGIApp, WebyApp
