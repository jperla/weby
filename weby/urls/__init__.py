from __future__ import absolute_import

from .parsers import UrlParse, intparse, remaining

def Url(object):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return self.url

    def __repr__(self):
        return self.url

