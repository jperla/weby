import weby

app = weby.defaults.App()

@app.default_subapp()
@weby.urlable_page(weby.urls.remaining())
def app(req, p, name):
    times = req.params.get(u'times', 1)
    print name.encode('utf8')
    for i in xrange(int(times)):
        p(u'Hello, %s!<br />' % (name or u'world'))

if __name__ == '__main__':
    weby.run(weby.wsgify(app))
