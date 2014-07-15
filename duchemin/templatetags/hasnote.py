from django.template.defaultfilters import register


@register.filter(name='hasnote')
def hasnote(user, piece):
	# Returns True iff the user has a note on a given piece.
    contains = False
    for note in user.notes.all():
        if note.piece == piece:
            contains = True
    return contains
