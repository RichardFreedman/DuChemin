from django.template.defaultfilters import register


@register.filter(name='isfavourite')
def isfavourite(user, piece):
    return user.profile.favourited_piece.filter(id=piece.id)
