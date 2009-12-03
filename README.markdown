Weby
======
The lazy man's web framework.


Purpose
=======
You have an awesome offline program.  Weby and deploy it in under _5_ minutes.


Example: a complete Weby application
======================================

    import weby

    app = weby.defaults.App()

    @app.default_subapp()
    @weby.urlable_page(weby.urls.remaining())
    def app(req, page, name):
        times = req.params.get('times', 1)
        for i in xrange(int(times)):
            page(u'Hello, %s!<br />' % (name or u'world'))

    if __name__ == '__main__':
        weby.run(weby.wsgify(app))

Programming and Design Philosophy
=================================

* The Zen of Python
* Don't repeat yourself
* Simplicity over features
* Clarity over cleverness
* Explicit is better than implicit
* No magic
* Make only Order of Magnitude improvements
* Defaults over options
* Innovation over patterns
* Exactly one obvious way to do anything
* Build bottom-up as well as top-down
* Code less
* Don't repeat yourself
* Automate everything
* No pagination

TODO
====
Weby already includes 

- Controllers
- Templates and helpers
- Beautiful Urls
- Smallest python webapps in production
- Very extensible and easy to understand
- Natural code layout using python packages
- A production server thread
- Error handling server thread
- Webapp testing framework
- Full Unicode compliance and safety
- Email framework

Weby still needs, in order,

- Documentation, auto-generated from codebase, with auto-tests
- Redo redirecters and page objects / templates

- Cache system

- Middleware
- Standard template filters
- Forms

- Sessions and authentication*
- CSRF protection

- Layout system for templates
- XSS Protection
- Internationalization*

- A debugging server thread
- Event-based server thread

- Pluggable sub-webapps
- Ecosystem of pluggable sub-webapps*

- Synchronous and asynchronous signals and dispatchers*

Requires some kind of data decision***:
- Models and backend storage*
- Auto-admin (databrowse?)*
- Sitemaps
- RSS Feeds
- Testing framework data fixtures

*requires a hard design decision


Weby will never have

* { Braces }
* Pagination
* Clunky design
* Repetition
* Repetition


ACKNOWLEDGEMENTS
================
Weby borrows heavily from existing Python web architectures 
and thanks them profusely for their high quality.

Thank you WebOb and Paste for much of this code.  
Also, thank you Ian Bicking, Django developers, and Guido van Rossum 
for great design ideas and a high standard of excellence.

API
===
I strive for a bug-free master branch.  

As to the stability of the API and backwards-compatibility, 
I guarantee nothing.  In fact, I guarantee that I will change
the API many times, breaking unmodified applications, sometimes
purposefully to keep you mindful.

I will keep this promise both through the beta and after 1.0.

Legacy code kills the pace of development, snowballs cruft, 
and holds back the possibility of game-changing improvements.

On the other hand, branches of point versions may be maintained
with bug fixes for those who want to stay secure, but do not need
new features.


License
=======
MIT license

