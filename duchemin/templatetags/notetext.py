from django.template.defaultfilters import register


@register.filter(name='notetext')
def notetext(user, piece):
	# Returns True iff the user has a note on a given piece.
    text = ''
    for note in user.notes.all().order_by("updated"):
    	# We will overwrite with most recent if there is more than one
        if note.piece == piece:
            text = note.text
    return text
