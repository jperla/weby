import weby
from weby.templates.helpers import html

@weby.template()
def apps(t):
    t(html.h2('Weby Apps'))
    t(html.h3('Philosophy'))
    with t(html.ul_block()):
        t(html.li('Everything is an app.  Simple.  Each dynamic page is an app.  Url dispatching/routing is an app. Serving static pages is an app.'))
    t(html.h3('Design'))
    t(html.p('An app is any callable which takes a request object as input, and returns a special iterator as output.'))
    t(html.p('Weby request object are the same as the standard WebOb request objects designed by Ian Bicking.  They are almost identical to Django and other Python web framework request objects.'))
    t(html.p('The iterator that returned by the app must begin with a 2-tuple of the (1) status code, and (2) a list of HTTP headers.  The rest of the iterator are unicode strings of the content of the HTTP response.  Here is a simple example:'))
    t(html.code_pre('''
        def hello_world(req):
            yield 200, ['Content-Type: text/html']
            yield u'<html>Hello, %s</html>' % req.params.get('name', '')
    '''))
    t(html.p('Of course, most apps will yield 200 responses. You may not want to type yield out all of the time.  Finally, you probably want an easier way to manage HTTP headers.  We can decorate the request to make it easier to use:'))
    t(html.code_pre('''
        @weby.page()
        def hello_world(req, page):
            page(u'<html>Hello, %s</html>' % req.params.get('name', ''))
    '''))
    t(html.p('Or equivalently, using the weby template helper html library:'))
    t(html.code_pre('''
        @weby.page()
        def hello_world(req, page):
            page(html.html(u'Hello, %s' % req.params.get('name', '')))
    '''))
    t(html.p('Of course, in real code, you should call a separate template function, which of course returns a unicode string:'))
    t(html.code_pre('''
        @weby.page()
        def hello_world(req, page):
            name = req.params.get('name', '')
            page(template_hello_world(name))
    '''))
    t(html.p('The decorator accumulates the response for the page, and then yields the correct iterator after your app returns.  See the ' + html.code('WebyPage') + ' documentation for more information about what you can do.  For example, you can use ' + html.code('page.redirect') + ' to send an HTTP 302 Redirect to another page'))


        
@weby.template()
def urls(t):
    t(html.h2('Weby Urls'))
    t(html.h3('Philosophy'))
    with t(html.ul_block()):
        t(html.li('Use what you know.  Use Python.  Do not learn a new url syntax.'))
        t(html.li('Link to other pages using code, not strings'))
        t(html.li('Put the urls with the controllers.  They go hand in hand'))
        t(html.li('Use Python.  Utilize the full turing-complete power of Python, not a limited syntax or even regexes.'))
    t(html.h3('Design'))
    t(html.p('First, remember that everything is an app.  Url dispatching (routing) is an app. It is simply an app which knows about other apps.  It takes a request, sees which of its subapps to send the request to, tells the app to process the request, and then returns the subapp\'s response back.'))
    t(html.p('Therefore, you can make your own url dispatching apps easily.  Weby comes with an url dispatch app which is very useful and simple.'))
    t(html.code_pre('''
        app = weby.apps.dispatch.SimpleDispatchApp()

        @app.subapp('hello')
        def hello_world(req)
            page(template_hello_world(req.params.get('name', '')))
    '''))
    t(html.p('If you run the app go to "/hello", you will see hello_world running as a subapp of the app, and it probably say something like "Hello, Weby!".'))
    t(html.p('The SimpleDispatchApp is actually Weby\'s default app and dispatching app.  You can nest apps as much as you want.'))
    t(html.code_pre('''
        main_app = weby.defaults.App()
        @app.subapp(''):
        def index(req)
            ...

        profiles_app = weby.defaults.App()
        @profiles_app.subapp('view')
        def view_profile(req):
            ...

        @profiles_app.subapp('edit')
        def edit_profile(req):
            ...

        main_app.subapp('profiles')(profiles_app)
    '''))
    t(html.p('With app running, you can go to the index at "/", but also "/profiles/view" and "/profiles/edit/" in the profiles_app since it is a subapp of main_app. You can see how this is useful for pluggable sub-webapps like blogs or forum software that is easy to integrate.'))
    t(html.p('But you can do even cooler things.  Instead of a slow and error-prone backwards induction to figure out the url of a page, or a hard-coded action/controller linking scheme, you can refer to controllers directly and ask them to tell you their url:'))
    t(html.code_pre('''
        hello_world.url()
    '''))
    t(html.p('You can even pass arguments:'))
    t(html.code_pre('''
        @profiles_app.subapp('view')
        @weby.urls.parse(weby.urls.intparse())
        def profile_view(req, id)
            user = User.find(id)
            page(template_view_profile(user))

        >>> print profile_view.url(3)
        "/profiles/view/3/"
    '''))
    t(html.p('And it can get arbitrarily complex:'))
    t(html.code_pre('''
        @profiles_app.subapp('view')
        @weby.urls.parse(weby.urls.intparse(), 
                         weby.urls.stringparse(), 
                         weby.urls.remainingparse())
        def profile_view(req, id, name, token)
            user = User.find(id)
            assert(user.token == token)
            page(template_view_profile(user, name))

        >>> print profile_view.url(3, 'John Doe', '5cf6cafef00d')
        "/profiles/view/3/John_Doe/5cf6cafef00d"
    '''))
        
    

@weby.template()
def templates(t):
    t(html.h2('Weby Templates'))
    t(html.h3('Philosophy'))
    with t(html.ul_block()):
        t(html.li('Learn as few new things as possible.  You know Python.  You know HTML.  You should not have to a new template language.'))
        t(html.li('Use the full power of Python.  Easily create loops, use temporary variables, build filters, and import partials,'))
        t(html.li('Separate presentation from logic. For best practices, explicitly pass only the necessary variables.  Enforce this by convention, not by cripling power.'))
    t(html.h3('Design'))
    t(html.p('Weby templates are very simple. '))
    t(html.code_pre('''
        @weby.template()
        def template_print_name(t, name):
            t(u'Hello, %s' % name)
    '''))
    t(html.p('The function ' + html.code('template_print_name') +
                ' returns an'
                ' iterator of unicode strings.'))
    t(html.p('The ' + html.code('weby.template') + ' decorator'
                ' adds a template'
                ' accumulator as the first argument, then returns'
                ' the accumulated array of strings at the end.'
                ' You can make an equivalent template function'
                ' without the decorator, but it will require some'
                ' repetitive code:'))
    t(html.code_pre('''
        def template_print_name(name):
            t = []
            t.append(u'Hello, %s' % name)
            return t
    '''))
    t(html.p('Also, the '
                ' accumulator only takes unicode strings to enforce'
                ' correctness in your application code. Weby helps'
                ' you avoid unicode errors.'))
    t(html.p('Also, if you pass the template accumulator a'
                ' 2-tuple, then it will return a context manager'
                ' for use with the ' + html.code('with') + ''
                ' statement.  For example, '))
    t(html.code_pre(html.h('''
        @weby.template()
        def template_print_name(t, name):
            with t((u'<div>',u'</div>')):
                t(u'Hello, %s' % name)
    ''')))
    t(html.p('which is just syntactic sugar for'))
    t(html.code_pre(html.h('''
        @weby.template()
        def template_print_name(t, name):
            t(u'<div>')
            t(u'Hello, %s' % name)
            t(u'</div>')
    ''')))
    t(html.p('Weby has many libraries to make this even'
                ' easier.  Weby has libraries for writing'
                ' XML, RSS, and HTML templates:'))
    t(html.code_pre('''
        from weby.templates.helpers import html

        @weby.template()
        def template_print_name(t, name):
            with t(html.div_block()):
                t(u'Hello, %s' % name)
    '''))
    t(html.p('Every html tag has a predictable function in Weby\'s'
                ' html library.  Also, each one can take an attribute'
                ' dictionary.  The library always returns unicode'
                ' strings, so you can nest them easily.'))
    t(html.code_pre('''
        from weby.templates.helpers import html

        @weby.template()
        def template_print_name(t, name):
            with t(html.html_block()):
                with t(html.body_block()):
                    with t(html.div_block({'id':'hello'})):
                            t(html.p('Hello, %s' % name,
                                        {'style':'font-weight:bold;'}))
                    with t(html.ul_block()):
                        for i in xrange(3):
                            t(html.li(html.a('Hello, %s' % i, 
                                                {'href':'/'})))
    '''))
    t(html.p('This generates the following html'))
    t(html.code_pre(html.h('''
        <html>
        <body>
        <div id="hello">
        <p style="font-weight:bold;">Hello, Weby</p>
        </div>
        <ul>
        <li><a href="/">Hello, 0</a></li>
        <li><a href="/">Hello, 1</a></li>
        <li><a href="/">Hello, 2</a></li>
        </ul>
        </body>
        </html>
    ''')))

@weby.template()
def index(t):
    with t(html.html_block()):
        with t(html.body_block({'style':'width:600px'})):
            t(html.h1('Weby'))
            t(templates())
            t(apps())
            t(urls())

print ''.join(weby.recursively_iterate(index()))
