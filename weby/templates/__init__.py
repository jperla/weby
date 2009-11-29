from __future__ import absolute_import

from . import helpers

def template():
    def decorator(f):
        class Catcher(object):
            def __init__(self, caught=None, start=u'', end=u''):
                if caught is None:
                    self.caught = []
                else:
                    self.caught = caught
                self.start = start
                self.end = [end]
            def __catch(self, s):
                self.caught.append(s)
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
                    self.caught.append(r)
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
        def new_f(*args, **kwargs):
            catcher = Catcher()
            f(catcher, *args, **kwargs)
            return catcher.caught
        return new_f
    return decorator
