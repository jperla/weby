#!/usr/bin/env python
import time

import weby

app = weby.defaults.App()

# Controllers
@app.subapp('/')
@weby.urlable_page()
def index(req, page):
    page(u'Hello, world!')

static_path = u'tests/apps/standard/static/'
static = app.subapp('static')(weby.apps.standard.static(static_path))
    

# Middleware
from weby.middleware import EvalException
wrapped_app = weby.wsgify(app, EvalException)

# Server
from weby.http import server
if __name__ == '__main__':
    server.serve(wrapped_app, host='127.0.0.1', port=8080)

