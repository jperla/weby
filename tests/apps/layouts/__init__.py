#!/usr/bin/env python
from __future__ import with_statement
import weby
from weby.templates.helpers import html

app = weby.defaults.App()

# Layout template
@weby.template()
def page_layout(p, title, inside):
    with p(html.html()):
        with p(html.head()):
            p(html.title(title))
        with p(html.body()):
            p(inside)


# Controllers
@app.subapp('hello')
@weby.urlable_page()
def hello(req, page):
    name = req.params.get(u'name', u'world')
    page(page_layout(u'Hello App', hello_template(name)))

# Templates
# This would normally be in a different file in a different module 
@weby.template()
def hello_template(p, name):
    with p(html.form({'action':'', 'method':'GET'})):
        p(u'Hello, %s! <br />' % name)
        p(u'Your name: %s' % html.input_text('name'))
        p(html.input_submit('name'))


# Middleware
from weby.middleware import EvalException
wrapped_app = weby.wsgify(app, EvalException)


# Server
if __name__ == '__main__':
    weby.http.server.serve(wrapped_app, host='127.0.0.1', port='8080')

