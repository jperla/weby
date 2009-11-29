from contextlib import contextmanager

from .. import http
import types

@contextmanager
def get(app, path, host='http://localhost'):
    assert(not isinstance(path, unicode), u'Must ask for encoded path')
    req = http.Request.blank(host + path)
    response = req.get_response(app)
    yield response

@contextmanager
def post(app, path, data, host='http://localhost'):
    assert(not isinstance(path, unicode), u'Must ask for encoded path')
    req = http.Request.blank(host + path)
    req.method = u'POST'
    for key in data:
        req.POST[key] = data[key]
    response = req.get_response(app)
    yield response


@contextmanager
def difference(f, amount=None, message=''):
    assert(isinstance(f, types.FunctionType), u'difference() takes a function to call as the first argument which it calls twice: once before and once after')
    original = f()
    yield
    new = f()
    if amount == None:
        assert(original != new)
    else:
        assert(new - original == amount)


