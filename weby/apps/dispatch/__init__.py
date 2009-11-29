from __future__ import absolute_import

import types
import logging
import wsgiref
from wsgiref import util

from ... import http as _http
from .. import WebyApp

class DispatchApp(WebyApp):
    def __init__(self):
        WebyApp.__init__(self)

    def __call__(self, req):
        app, req = self.dispatched_app_and_request(req)
        return app(req)

    def dispatched_app_and_request(req, p):
        # returns (app, req)
        raise NotImplementedError

    def subapp(self, *args, **kwargs):
        def subapp_decorator(subapp):
            subapp.parent = self
            self.register_subapp(subapp, *args, **kwargs)
            return subapp
        return subapp_decorator

    def register_subapp(self, subapp):
        raise NotImplementedError

    def wrap_url(self, subapp, suburl):
        url = self.parented_url(subapp, suburl)
        if self.parent is None:
            return url
        else:
            return self.parent.wrap_url(self, url)

    def parented_url(self, subapp, suburl):
        raise NotImplementedError




class SimpleDispatchApp(DispatchApp):
    def __init__(self, default=None):
        self.default = default
        self.apps, self.urls = {}, {}
        DispatchApp.__init__(self)

    def default_subapp(self, *args, **kwargs):
        assert(self.default is None)
        def subapp_decorator(subapp):
            assert(subapp.parent is None)
            subapp.parent = self
            self.default = subapp
            return subapp
        return subapp_decorator

    def dispatched_app_and_request(self, req):
        path_info = req.environ[u'PATH_INFO'] #for debugging
        #TODO: jperla: deep copy request here?
        name = u'%s' % req.path_info.lstrip('/').split('/', 1)[0]
        apps = self.apps
        app = apps.get(name, None)
        if app is not None:
            wsgiref.util.shift_path_info(req.environ)
            return app, req
        else:
            if self.default is not None:
                return self.default, req
            else:
                raise _http.status.not_found()

    def register_subapp(self, subapp, path):
        if path in self.apps:
            raise Exception(u'Already dispatching to path: %s' % path)
        self.apps[path] = subapp
        self.urls[subapp] = path

    def parented_url(self, subapp, suburl):
        assert(subapp in self.urls or subapp == self.default)
        #TODO: jperla: fix index urls
        if subapp == self.default:
            return suburl
        else:
            return (u'/' + self.urls[subapp] + suburl).replace(u'//', u'/')


