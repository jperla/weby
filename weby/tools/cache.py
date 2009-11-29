import time as _time

class Cache(object):
    def __init__(self):
        raise NotImplementedError
    def set(self, key, value, time=0):
        raise NotImplementedError
    def get(self, key):
        raise NotImplementedError
    def delete(self, key):
        raise NotImplementedError
    def delete_multi(self, keys):
        for key in keys:
            self.delete(key)
    def set_multi(self, mapping, time=0):
        for key in mapping:
            self.set(key, mapping[key], time)
        return True
    def get_multi(self, keys):
        return dict([(key, self.get(key)) for key in keys])
    def incr(self, key, delta=1):
        if self.get(key) is None:
            return None
        else:
            try:
                value = int(self.get(key))
            except ValueError, e:
                return None
            finally:
                new_value = value + delta
                self.set(str(new_value))
                return new_value
    def decr(self, key, delta=1):
        return self.incr(key, -delta)
    def add(self, key, val, time=0):
        if self.get(key) is None:
            return self.set(key, val, time)
        else:
            return None
    def replace(self, key, val, time=0):
        if self.get(key) is not None:
            return self.set(key, val, time)
        else:
            return None
    def cached(self, key, f, time=0):
        found = self.get(key)
        if not found:
            cached = f()
            self.set(key, cached)
            return cached
        else:
            return found

class MemoryCache(Cache):
    def __init__(self):
        self.cache = {}
    def delete(self, key):
        del(self.cache[key])
        return True
    def set(self, key, value, time=0):
        if time == 0:
            time = 1000000000
        now = _time.time()
        self.cache[key] = (now + time, value)
        return True
    def get(self, key):
        now = _time.time()
        if key in self.cache:
            expires, value = self.cache[key]
            if now > expires:
                return value
            else:
                return None
        else:
            return None

class DummyCache(Cache):
    def __init__(self):
        pass
    def delete(self, key):
        return True
    def get(self, key):
        return None
    def set(self, key, value, time=0):
        return True

class MemcachedCache(Cache):
    def __init__(self, locations):
        self.memcache_client = memcache.Client(locations)
    def set(self, key, value, time=0):
        self.memcache_client.set(key, time=time)
        return True
    def get(self, key):
        return self.memcache_client.get(key)
    def delete(self, key):
        v = self.memcache_client.delete(key)
        return True if v != 0 else False
    def add(self, key, value, time=0):
        v = self.memcache_client.add(key, value, time=time)
        return True if v != 0 else False
    def replace(self, key, value, time=0):
        v = self.memcache_client.replace(key, value, time=time)
        return True if v != 0 else False
    def get_multi(self, keys):
        return self.memcache_client.get_multi(keys)
    def delete_multi(self, keys):
        return self.memcache_client.delete_multi(keys)
    def set_multi(self, mapping, time):
        return self.memcache_client.set_multi(keys)
    def incr(self, key):
        return self.memcache_client.incr(key)
    def decr(self, key):
        return self.memcache_client.decr(key)

        
