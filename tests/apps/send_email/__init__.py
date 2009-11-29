import webify

app = webify.apps.SingleApp()

@app.subapp()
@webify.urlable()
def send(req, p):
    email = req.params.get(u'email', u'nobody@jperla.com')
    mail_server = req.settings[u'mail_server']
    message = webify.email.create_text_message(u'nobody@jperla.com',
                                                [email],
                                                u'Hello, World!',
                                                u'I am sending you a text message')
    mail_server.send_message(message)
    p(u'Sent email.')

# Middleware
from webify.middleware import SettingsMiddleware

mail_server = webify.email.TestMailServer()
settings = {'mail_server': mail_server}
wrapped_app = webify.wsgify(app, SettingsMiddleware(settings))


if __name__ == '__main__':
    webify.run(wrapped_app)
    
# Try Loading http://127.0.0.1:8080/hello/world?times=1000000
