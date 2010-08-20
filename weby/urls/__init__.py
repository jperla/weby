from __future__ import absolute_import

from .parsers import UrlParse, intparse, remaining

import urllib

class Url(object):
    def __init__(self, url, q={}):
        if isinstance(url, Url):
            self.url = url.url
            self._q = url._q
        else:
            self.url = url
            self._q = q

    def q(self, d):
        new_q = dict([(k,v) for k,v in self._q] + [(k,v) for k,v in d.iteritems()])
        return Url(self.url, new_q)

    def __add__(self, s):
        return Url(self.url + s, self._q)

    def __str__(self):
        base = self.url
        def encode(k):
            k,v = urllib.quote(k), urllib.quote(self._q[k])
            return  '%s=%s' % (k, v)
        if len(self._q) > 0:
            qp = '&'.join(encode(f) for f in self._q)
            relative_url = '%s?%s' % (base, qp)
        else:
            relative_url = base
        #TODO: jperla: add host domain
        url = relative_url
        return url

    def __repr__(self):
        return str(self)

