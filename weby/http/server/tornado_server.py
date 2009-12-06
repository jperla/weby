import urllib

import webob

import tornado.httpserver
import tornado.ioloop
import tornado.web

def wrap_tornado(app):
    def new(tornado_request):
        args = '&'.join('%s=%s' % (k,urllib.quote(v[0])) for k,v in tornado_request.arguments.iteritems())
        req = webob.Request.blank(tornado_request.path + '?' + args)
        body = app(req)
        status, headers = body.next()
        content = ''.join(body)
        #TODO: jperla: make this return 404 appropriately
        tornado_request.write("HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s" % (
                        len(content), content))
        tornado_request.finish()
    return new

def start(app, host=None, port=8088):
    #TODO: jperla: make sure sending correct app type
    #assert(type(app) != WSGIApp)
    tornado_app = wrap_tornado(app)
    http_server = tornado.httpserver.HTTPServer(tornado_app)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

