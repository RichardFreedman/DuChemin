from django.template.defaultfilters import register


@register.filter(name='notetext')
def notetext(user, piece):
    # Returns the text of a note, if there is one; else return empty string
    notes = user.notes.filter(piece=piece).order_by("-updated")
    text = ''
    if notes:
        text = notes[0].text
    return text
