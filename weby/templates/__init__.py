from __future__ import absolute_import

from . import helpers

def recursively_iterate(item):
    if isinstance(item, str):
        raise Exception(u'Always work with unicode within your app: %s', item)
    elif isinstance(item, unicode):
        yield item
    else:
        for subitem in item:
            for i in recursively_iterate(subitem):
                yield i

def join(f):
    '''Decorator which recursively iterate over a template to join it'''
    def decorated(*args, **kwargs):
        return u''.join(recursively_iterate(f(*args, **kwargs)))
    return decorated

def joined(*targs, **tkwargs):
    '''Template that comes out joined into one string'''
    def decorator(f):
        return join(template(*targs, **tkwargs)(f))
    return decorator
    
class Accumulator(object):
    def __init__(self, accumulated=None, start=u'', end=u''):
        if accumulated is None:
            self.accumulated = []
        else:
            self.accumulated = accumulated
        self.start = start
        self.end = [end]
    def __catch(self, s):
        self.accumulated.append(s)
    def __call__(self, r):
        if isinstance(r, unicode):
            self.__catch(r)
        elif isinstance(r, tuple) and len(r) == 2:
            start, end = r
            assert(isinstance(start, unicode))
            assert(isinstance(end, unicode))
            self.start = start
            self.end.insert(0, end)
            return self
        elif isinstance(r, str):
            #TODO: jperla: unify this
            raise Exception('Always output unicode: %s' % r)
        else:
            # This is an array (sub-template), just append
            self.accumulated.append(r)
    '''
            # Hide this since recursive_iterate checks, 
            # and we dont check here anyway
            raise Exception('Unknown parameter, try t.sub(): %s', r)
    def sub(self, t):
    '''
    def __enter__(self):
        self.__catch(self.start)
        return self
    def __exit__(self, type, value, tb):
        self.__catch(self.end[0])
        del(self.end[0])

def _sanitize_lib(lib):
    class new_lib(object):
        def __init__(self, lib):
            self._lib = lib
        def __hasattr__(self, x):
            return True
        def __getattr__(self, x):
            def new_attr(*a):
                args = None
                if len(a) == 1 and isinstance(a[0], tuple) and len(a[0]) == 2:
                    args, sanitized = a
                    if not sanitized and len(args) > 0:
                        args[0] = self._lib.sanitize(args[0])
                else:
                    args = a
                    if len(args) > 0:
                        args[0] = self._lib.sanitize(args[0])
                return (getattr(self._lib, x)(*args), False)
            return new_attr
    return new_lib(lib)

def safe_template(lib):
    def decorator(f):
        def new_f(*args, **kwargs):
            accumulator = Accumulator()
            def new_call(*a):
                text = None
                if len(a) == 1 and isinstance(a[0], tuple) and len(a[0]) == 2:
                    text, sanitized = a[0]
                    if not sanitized:
                        text = lib.sanitize(text)
                else:
                    text = lib.sanitize(text)
                accumulator.__call__(text)
            accumulator.__call__ = new_call
            f(accumulator, _sanitize_lib(lib), *args, **kwargs)
            return accumulator.accumulated
        return new_f
    return decorator

def template():
    def decorator(f):
        def new_f(*args, **kwargs):
            accumulator = Accumulator()
            f(accumulator, *args, **kwargs)
            return accumulator.accumulated
        return new_f
    return decorator
