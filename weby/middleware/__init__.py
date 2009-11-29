from paste.evalexception import EvalException

def install_middleware(app, middleware):
    for m in middleware:
        app = m(app)
    return app

class SettingsMiddleware(object):
    '''
    Takes a dictionary of aribtrary settings for the app.
    Places the dictionary at the top of a stack 
    in the environ (key "settings")
    '''
    def __init__(self, settings):
        self.settings = settings

    def __call__(self, app):
        def wrapper(environ, start_response):
            if u'settings' in environ:
                environ[u'settings'].insert(self.settings, 0)
            else:
                environ['settings'] = [self.settings]
            return app(environ, start_response)
        return wrapper 

