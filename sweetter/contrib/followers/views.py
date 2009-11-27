from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from sweetter.contrib.followers.models import Follower
from sweetter.ublogging.models import Post, User
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

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
