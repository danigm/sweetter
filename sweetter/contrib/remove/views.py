from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from sweetter.ublogging.models import Post, User
from django.contrib.auth.decorators import login_required

@login_required
def remove(request, postid):
    if (request.user.is_authenticated()):
        u = request.user
        p = Post.objects.get(id=postid)
        if p.user == u:
            p.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

