import weby

app = weby.defaults.App()

@app.default_subapp()
@weby.urlable_page()
def send(req, page):
    email = req.params.get(u'email', u'nobody@jperla.com')
    mail_server = req.settings[u'mail_server']
    message = weby.email.create_text_message(u'nobody@jperla.com',
                                                [email],
                                                u'Hello, World!',
                                                u'I am sending you a text message')
    mail_server.send_message(message)
    page(u'Sent email.')

mail_server = weby.email.TestMailServer()
settings = {'mail_server': mail_server}
app = weby.apps.SettingsApp(settings, app)

if __name__ == '__main__':
    weby.run(weby.wsgify(app))
    
# Try Loading http://127.0.0.1:8080/hello/world?times=1000000
