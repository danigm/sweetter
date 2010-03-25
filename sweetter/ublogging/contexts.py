from django.contrib.flatpages.models import FlatPage

from ublogging.models import Profile


def profile(request):
    if request.user.is_authenticated():
        profile = Profile.objects.get(user=request.user)
        return {'user_profile': profile}

    return  {}

def flatpages(request):
    return {'flatpages': FlatPage.objects.all()}
