#!/usr/bin/env python
import time

import weby

app = weby.defaults.App()

# Controllers
@app.subapp('')
@weby.urlable_page()
def index(req, page):
    page(u'Hello, world!')

@app.subapp('hello')
@weby.urlable_page()
def hello(req, page):
    page(u'<form method="POST">')
    name = req.params.get('name', None)
    if name is None:
        page(u'Hello, world! <br />')
    else:
        page(u'Hello, %(name)s! <br />' % {'name': name})
    page(u'Your name: <input type="text" name="name">')
    page(u'<input type="submit">')
    page(u'</form>')

@app.subapp('hello_old')
@weby.urlable_page()
def hello_old(req, p):
    weby.http.status.redirect(hello.url())

# Middleware
from weby.middleware import EvalException
wrapped_app = weby.wsgify(app, EvalException)

# Server
from weby.http import server
if __name__ == '__main__':
    server.serve(wrapped_app, host='127.0.0.1', port=8080)

