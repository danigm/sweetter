from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from contrib.followers.models import Follower
from ublogging.models import User


@login_required
def follow(request, user_id):
    u=User.objects.get(id=user_id)
    f = Follower.objects.filter(user=u, follower=request.user)
    if f:
        f.delete()
    else:
        f=Follower(user = u, follower = request.user)
        f.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
