#!/usr/bin/env python
import time

import webify

app = webify.defaults.app()

# Controllers
@app.subapp(path='/')
@webify.urlable()
def index(req, p):
    p(u'Hello, world!')

static_path = u'tests/apps/standard/static/'
static = app.subapp(path='/static')(webify.apps.standard.static(static_path))
    

# Middleware
from webify.middleware import EvalException
wrapped_app = webify.wsgify(app, EvalException)

# Server
from webify.http import server
if __name__ == '__main__':
    server.serve(wrapped_app, host='127.0.0.1', port=8080)

