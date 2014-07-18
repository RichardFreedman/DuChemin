from django.template.defaultfilters import register


@register.filter(name='notetext')
def notetext(user, piece):
    # Returns the text of a note, if there is one; else return empty string
    text = ''
    for note in user.notes.all().order_by("updated"):
        # We will overwrite with most recent if there is more than one
        if note.piece == piece:
            text = note.text
    return text
