from django.template.defaultfilters import register


@register.filter(name='apostrophe')
def apostrophe(string):
    return str(string).replace("'", "\u2019")
