from django.template.defaultfilters import register


@register.filter(name='figuredash')
def figuredash(string):
    return unicode(string).replace(u"-", u"\u2013")
