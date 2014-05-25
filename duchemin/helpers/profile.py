from duchemin.models.userprofile import DCUserProfile


def get_or_create_profile(request):
    profile = None
    user = request.user
    try:
        profile = user.get_profile()
    except DCUserProfile.DoesNotExist:
        profile = DCUserProfile.objects.create(user=user)
    return profile
