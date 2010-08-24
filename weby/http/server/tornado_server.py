from __future__ import absolute_import

import os
import sys
import urllib
import urlparse
import cStringIO

from ...lib import webob

#TODO: jperla: import local tornado, and if 
# that fails use this tornado
from ...lib import tornado

import tornado.httpserver
import tornado.ioloop
import tornado.web

from ...http import reason_phrases

def wrap_tornado(app):
    def new(tornado_request):
        #TODO: jperla: wrap into complete wsgi-like request
        #args = '&'.join('%s=%s' % (urllib.quote(k),urllib.quote(v[0])) for k,v in tornado_request.arguments.iteritems())
        req = webob_request_from_tornado_request(tornado_request)
        body = app(req)
        status, headers = body.next()
        #TODO: jperla: make this return 404 appropriately
        status_line = 'HTTP/1.1 %s\r\n' % status
        headers = ''.join(['%s: %s\r\n' % h for h in headers])
        if isinstance(headers, unicode):
            #TODO: jperla: assumed utf8?
            headers = headers.encode('utf-8')
        content = ''.join(body)
        content_length = 'Content-Length: %d\r\n' % len(content) if len(content) > 0 else ''
        top = status_line + content_length + headers + '\r\n'
        assert isinstance(top, str), '%s, %s is not a str' % (type(top), top)
        tornado_request.write(top)
        if len(content) > 0:
            assert isinstance(content, str), '%s, %s is not a str' % (type(content), content)
            tornado_request.write(content);
        #for b in body:
        #    tornado_request.write(b)
        #TODO: jperla: make this iterate?
        tornado_request.finish()
    return new

def webob_request_from_tornado_request(tornado_request):
    #return webob.Request.blank(tornado_request.uri)
    environ = wsgi_environ_from_tornado_request(tornado_request)
    req = webob.Request(environ)
    return req


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

    environ['wsgi.errors'] = sys.stderr
    environ['wsgi.multithread'] = True
    environ['wsgi.multiprocess'] = True
    environ['wsgi.run_once'] = False
    environ['PWD'] = os.getcwd()
    for h,v in tornado_request.headers.iteritems():
        environ['HTTP_%s' % h.upper().replace('-', '_')] = v

    environ['wsgi.input'] = cStringIO.StringIO(tornado_request.body)
    if 'HTTP_CONTENT_LENGTH' in environ:
        environ['CONTENT_LENGTH'] = environ['HTTP_CONTENT_LENGTH']
    else:
        environ['CONTENT_LENGTH'] = len(tornado_request.body)
    if 'HTTP_CONTENT_TYPE' in environ:
        environ['CONTENT_TYPE'] = environ['HTTP_CONTENT_TYPE']
    return environ

def start(app, host=None, port=8088, num_processes=1):
    assert not isinstance(app, WSGIApp), 'Tornado server does not support WSGIApps'
    assert isinstance(app, WebyApp), 'Tornado server wrapper supports WebyApps'
    tornado_app = wrap_tornado(app)
    http_server = tornado.httpserver.HTTPServer(tornado_app)
    http_server.listen(port)
    try:
        tornado.ioloop.IOLoop.instance().start(num_processes)
    except:
        print 'Starting only one process...'
        # probably using old tornado version
        tornado.ioloop.IOLoop.instance().start()

serve = start

from ...apps import WSGIApp, WebyApp
