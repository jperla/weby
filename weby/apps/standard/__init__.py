from __future__ import absolute_import
import os

from ...lib import chardet
import codecs

from .. import urlable, page, WebyApp
from ... import urls
from ...http import status, defaults
from ...http.headers import content_types
import mimetypes

def HTTP404App():
    def f(req):
        headers = list(defaults.status_and_headers[1].iteritems())
        yield '404 Not Found', headers
        yield 'Page not found'
    return f

def static(file_root):
    '''
    static = app.subapp('static')(weby.apps.standard.static('static/'))
    '''
    @urlable(urls.remaining())
    def static(req, filename):
        # #TODO: jperla: Note: security problem
        path = os.path.join(file_root, filename)
        if os.path.exists(path) and os.path.isfile(path):
            #TODO: jperla: cache the static stuff forever
            #TODO: jperla: switch on image type
            content_type, encoding = mimetypes.guess_type(path, strict=False)
            headers = [('Content-Type', content_type)]
            if encoding is not None:
                headers += [('Content-Encoding', encoding)]
            yield '200 OK', headers
            #TODO: jperla: make this read and return in chunks
            if content_type.startswith('text'):
                data = codecs.open(path, 'r', 'utf-8').read().encode('utf-8')
            else:
                data = open(path, 'rb').read()
            yield data
        else:
            #TODO: jperla: weby is not defined; namespace it
            yield http.status.not_found()
    return static



