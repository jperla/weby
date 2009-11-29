#!/usr/bin/env python
from __future__ import with_statement
import webify
from webify.templates.helpers import html

# Layout template
@webify.template()
def page_layout(p, title, inside):
    with p(html.html()):
        with p(html.head()):
            p(html.title(title))
        with p(html.body()):
            p.sub(inside)

app = webify.defaults.app()

# Controllers
@app.subapp()
@webify.urlable()
def hello(req, p):
    name = req.params.get(u'name', u'world')
    p(page_layout(u'Hello App', hello_template(name)))

# Templates
# This would normally be in a different file in a different module 
@webify.template()
def hello_template(p, name):
    with p(html.form(action=u'', method='GET')):
        p(u'Hello, %s! <br />' % name)
        p(u'Your name: %s' % html.input_text('name'))
        p(html.input_submit('name'))


# Middleware
from webify.middleware import EvalException
wrapped_app = webify.wsgify(app, EvalException)


# Server
if __name__ == '__main__':
    webify.http.server.serve(wrapped_app, host='127.0.0.1', port='8080')

