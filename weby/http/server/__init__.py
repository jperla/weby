import logging

import wsgiref
def wsgiref_serve(app, host, port, reload=False):
    if reload:
        raise Exception('wsgiref server does not have reloading option')
    from wsgiref.simple_server import make_server
    httpd = make_server(host, port, app)
    httpd.serve_forever()
serve = wsgiref_serve 


'''
# jperla: Ignore paste for now because it sucks
try:
    import paste
except ImportError, e:
    logging.info('paste could not be imported')
else:
    def paste_serve(app, host, port, reload=False):
        if reload:
            raise Exception('paste server does not have reloading option')
        from paste import httpserver
        httpserver.serve(app, host=host, port=port)
    serve = paste_serve
'''

try:
    import cherrypy
except ImportError, e:
    logging.info('CherryPy could not be imported')
else:
    def cherrypy_serve(app, host, port, reload=False):
        if reload:
            raise Exception('cherrypy server does not have reloading option')
        from cherrypy import wsgiserver
        s = wsgiserver.CherryPyWSGIServer((host, port), app)
        try:
            s.start()
        except KeyboardInterrupt:
            s.stop()
    serve = cherrypy_serve


try:
    import werkzeug
except ImportError, e:
    logging.info('werkzeug could not be imported')
else:
    def werkzeug_serve(app, host, port, reload=False):
        werkzeug.run_simple(host, port, app, use_reloader=reload)
    serve = werkzeug_serve
        

        
