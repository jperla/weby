from __future__ import absolute_import

from . import charsets as __charsets

def content_type(type):
    return ('Content-Type', type)

html = content_type('text/html')
plain = content_type('text/plain')

css = content_type('text/css')

html_utf8 = content_type('text/html; %s' % __charsets.utf8)

image_gif = content_type('image/gif')
image_jpeg = content_type('image/jpeg')
image_png = content_type('image/png')

