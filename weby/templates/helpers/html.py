from contextlib import contextmanager
import itertools


def nobreaks(text):
    return (u'%s' % text).replace(u' ', u'&nbsp;')

def sanitize(text):
    #TODO: jperla: should sanitize html
    return (u'%s' % text).replace(u'<', u'&lt;')
h = sanitize

def escape_javascript(js):
    #TODO: jperla: should escape js
    return js

def __attribute_html(attrs):
    attribute_html = u' '.join(u'%s="%s"' % (k, v) 
                            for k,v in attrs.iteritems() if v is not None)
    if attribute_html != u'':
        attribute_html = u' ' + attribute_html
    return attribute_html

def _generate_element(open, end_open, close, default_attrs):
    def new_element(html, attrs={}):
        attrs = __merge(default_attrs, attrs)
        attribute_html = __attribute_html(attrs)
        if html is not None:
            # Remove newline if the previous html already has one
            #html = html[:-1] if html.endswith('\n') else html
            #return u'%s%s%s%s%s\n' % (open, attribute_html, end_open, html, close)
            return u'%s%s%s%s%s' % (open, attribute_html, end_open, html, close)
        else:
            #return u'%s%s />\n' % (open, attribute_html)
            return u'%s%s />' % (open, attribute_html)
    return new_element

def _generate_tag(name, attrs={}):
    return _generate_element(u'<%s' % name, u'>', u'</%s>' % name, attrs)



def a_href(href=None, text='', attrs={}):
    attrs['href'] = href
    options = u' '.join(u'%s="%s"' % (k, attrs[k]) for k in attrs)
    return u'<a %(options)s>%(text)s</a>' % { u'text':text, u'options':options}

def br():
    return u'<br />\n'
def hr():
    return u'<hr />\n'


span_smaller = _generate_tag(u'span', {u'style':'font-size:smaller;'})

script_src = lambda src: _generate_tag(u'script', 
                                       {u'type':u'text/javascript', 
                                        u'src':src})(u'')

link_css = lambda href,media=u'screen': _generate_tag(u'link', 
                                                      {u'type':u'text/css', 
                                                       u'rel':u'Stylesheet',
                                                       u'media':media,
                                                       u'href':href})(None)

def _generate_container(open, end_open, close, default_attrs={}):
    def new_container(attrs={}):
        attrs = __merge(default_attrs, attrs)
        attribute_html = u' '.join(u'%s="%s"' % (k, v) 
                                for k,v in attrs.iteritems() if v is not None)
        if attribute_html != u'':
            attribute_html = u' ' + attribute_html
        return (open + attribute_html + end_open, close)
    return new_container

def _generate_block_tag(tag_name, default_attrs={}):
    return _generate_container(u'<%s' % tag_name, 
                               u'>\n', 
                               u'</%s>\n' % tag_name,
                               default_attrs)

no_arg = object()
def _html_element(tag):
    def any_element(first=no_arg, attr=no_arg):
        #TODO: jperla: optimize? pre-compile?
        if attr == no_arg and (first == no_arg or isinstance(first, dict)):
            attr = first
            if attr == no_arg:
                return _generate_block_tag(tag)({})
            else:
                assert isinstance(attr, dict), '%s not a dict' % attr
                return _generate_block_tag(tag)(attr)
        else:
            if attr == no_arg:
                return _generate_element('<%s' % tag, '>', '</%s>' % tag, {})(first, {})
            else:
                assert isinstance(attr, dict), '%s not a dict' % attr
                return _generate_element('<%s' % tag, '>', '</%s>' % tag, {})(first, attr)
    return any_element

#TODO: jperla: find all tags
__all_html_tags = [
'h1', 'h2', 'h3', 'h4', 'h5',
'p', 'b', 'a', 'em', 'i', 'ol', 'ul', 'li', 
'table', 'thead', 'tbody', 'tr', 'th', 'td',
'img', 'span', 'div', 'code', 'pre',
'html', 'head', 'body', 'title', 'meta', 'link', 'script',
'form', 'textarea', 'input', 'button',
]
for tag in __all_html_tags:
    #TODO: jperla: dont use exec for this
    exec('%s = _html_element("%s")' % (tag, tag))

#TODO: jperla: pre code broken for with statement
pre_code = _generate_element('<pre', '><code>','</code></pre>', {})

'''
def h1(text):
    return u'<h1>%s</h1>\n' % h(text)

def h2(text):
    return u'<h2>%s</h2>\n' % h(text)

def h3(text):
    return u'<h3>%s</h3>\n' % h(text)


li = _generate_tag(u'li')
p = _generate_tag(u'p')
td = _generate_tag(u'td')
th = _generate_tag(u'th')
b = _generate_tag(u'b')
i = _generate_tag(u'i')
em = _generate_tag(u'em')
title = _generate_tag(u'title')
span = _generate_tag(u'span')
img = lambda src, attrs={}: _generate_tag(u'img')(u'', __merge({'src':src}, attrs))


html = _generate_block_tag(u'html')
body = _generate_block_tag(u'body')
tr = _generate_block_tag(u'tr')
table = _generate_block_tag(u'table')
thead = _generate_block_tag(u'thead')
tbody = _generate_block_tag(u'tbody')
ol = _generate_block_tag(u'ol')
ul = _generate_block_tag(u'ul')
head = _generate_block_tag(u'head')
div = _generate_block_tag(u'div')
button = _generate_block_tag(u'button')
p_block = _generate_block_tag(u'p')
li_block = _generate_block_tag(u'li')
td_block = _generate_block_tag(u'td')
def textarea(name=None, id=None, attrs={}):
    attrs = __merge({'name':name, 'id':id}, attrs)
    return _generate_block_tag(u'textarea', attrs)()
def form(action=u'', method=u'POST', attrs={}):
    attrs = __merge({'action':action, 'method':method}, attrs)
    return _generate_block_tag(u'form', attrs)()
'''




def __merge(d1, d2):
    #assert isinstance(d1, dict), '%s not a dict' % d1
    #assert isinstance(d2, dict), '%s not a dict' % d2
    return dict([(k,v) for k,v in itertools.chain(d1.iteritems(), d2.iteritems())])

input = lambda attrs: _generate_tag(u'input',
                                    __merge({u'type':u'text'}, attrs))(None)

def _generate_input(type):
    def new_input(name=None, value=None, id=None, attrs={}):
        return input(__merge({u'type':type,
                              u'name':name,
                              u'value':value,
                              u'id':id,}, attrs))
    return new_input

input_text = _generate_input(u'text')
input_submit = _generate_input(u'submit')
input_password = _generate_input(u'password')
input_hidden = _generate_input(u'hidden')
input_file = _generate_input(u'file')
#TODO: jperla: do elements for all html4/5
#TODO: jperla: ignore end tags and quotes??

def input_radio(name=None, value=None, id=None, attrs={}):
    attrs = __merge({'name':name, 'value':value, 'id':id, 'type':'radio'}, attrs)
    return _generate_block_tag(u'input', attrs)()

script_block = _generate_container(u'<script',
                                   u'><!--', 
                                   u'--></script>\n',
                                   {u'type':u'text/javascript'})

