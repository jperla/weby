from __future__ import absolute_import

import urllib

import webob

import tornado.httpserver
import tornado.ioloop
import tornado.web

def wrap_tornado(app):
    def new(tornado_request):
        #TODO: jperla: wrap into complete wsgi-like request
        args = '&'.join('%s=%s' % (urllib.quote(k),urllib.quote(v[0])) for k,v in tornado_request.arguments.iteritems())
        req = webob.Request.blank(tornado_request.path + '?' + args)
        body = app(req)
        status, headers = body.next()
        content = ''.join(body)
        #TODO: jperla: make this return 404 appropriately
        tornado_request.write("HTTP/1.1 200 OK\r\nContent-Type:text/html\r\nContent-Length: %d\r\n\r\n%s" % (
                        len(content), content))
        #TODO: jperla: make this iterate?
        tornado_request.finish()
    return new

def start(app, host=None, port=8088):
    assert not isinstance(app, WSGIApp), 'Tornado server does not support WSGIApps'
    assert isinstance(app, WebyApp), 'Tornado server wrapper supports WebyApps'
    tornado_app = wrap_tornado(app)
    http_server = tornado.httpserver.HTTPServer(tornado_app)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

from ...apps import WSGIApp, WebyApp
