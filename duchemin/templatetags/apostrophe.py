from django.template.defaultfilters import register


@register.filter(name='apostrophe')
def apostrophe(string):
    return unicode(string).replace(u"'", u"\u2019")
