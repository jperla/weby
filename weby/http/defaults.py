from __future__ import absolute_import

from .headers import content_types as __content_types
from .headers import charsets as __charsets
from . import status as __status

status = __status.ok
content_type = __content_types.html_utf8
headers = [
            content_type,
          ]

status_and_headers = status, headers
