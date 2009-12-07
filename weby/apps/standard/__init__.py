from __future__ import absolute_import
import os

import chardet
import codecs

from .. import urlable, page, WebyApp
from ... import urls
from ...http import status
from ...http.headers import content_types

def HTTP404App():
    def f(req):
        headers = [content_types.html_utf8]
        yield 404, headers
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
            headers = [content_types.image_png]
            yield 200, headers
            #TODO: jperla: make this read in chunks
            encoding = 'raw_unicode_escape'#chardet.detect(path)['encoding']
            yield codecs.open(path, 'rb', encoding).read()
            #yield open(path, 'rb').read()
        else:
            #TODO: jperla: weby is not defined; namespace it
            p(http.status.not_found())
    return static



