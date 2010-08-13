
__no_content = object()
def node(element_name, content=__no_content, attributes={}):
    attrs_string = _attrs_string(attributes)
    if content == __no_content:
        return node_block(element_name, attributes)
    else:
        return node_inline(element_name, content, attributes)

def _attrs_string(attributes):
    attrs = u' '.join(['%s="%s"' % (k,v) for k,v in attributes.iteritems()])
    attrs_string = (u' ' + attrs) if len(attrs) > 0 else u''
    return attrs_string

def node_inline(element_name, content, attributes={}):
    attrs_string = _attrs_string(attributes)
    if content == u'':
        return u'<%s%s />' % (element_name, attrs_string)
    else:
        return u'<%s%s>%s</%s>\n' % (element_name, attrs_string, content, element_name)

def node_block(element_name, attributes={}):
    attrs_string = _attrs_string(attributes)
    return u'<%s%s>\n' % (element_name, attrs_string), u'</%s>\n' % element_name

def cdata(content):
    return  u'<![CDATA[>%s\n]]>' % content
    
def cdata_block():
    return u'<![CDATA[>', u'\n]]>'
    
