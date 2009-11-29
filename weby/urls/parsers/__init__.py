class UrlParse(object):
    def __init__(self):
        pass
    def parse(self, req, url):
        ''' Returns (new_args, new_url)'''
        raise NotImplementedError
    def generate(self, req, args, url):
        ''' Returns (new_args, new_url)'''
        raise NotImplementedError
    
class intparse(UrlParse):
    def parse(self, req, url):
        assert(url.startswith('/'))
        nothing, i, rest = url.split('/', 2)
        rest = u'/%s' % rest
        try:
            i = int(i)
        except ValueError, e:
            return [None], rest
        else:
            return [i], rest

    def generate(self, args, url):
        assert(len(args) > 0)
        return args[1:], u'%s%s/' % (url, args[0])


class remaining(UrlParse):
    def parse(self, req, url):
        assert(url.startswith('/'))
        return url[1:]

    def generate(self, args, url):
        assert(len(args) == 1)
        return [], u'%s%s' % (url, args[0])
