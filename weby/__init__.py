from __future__ import absolute_import

from .templates import template

def recursively_iterate(item):
    if isinstance(item, str):
        raise Exception(u'Always work with unicode within your app: %s', item)
    elif isinstance(item, unicode):
        yield item
    else:
        for subitem in item:
            for i in recursively_iterate(subitem):
                yield i

