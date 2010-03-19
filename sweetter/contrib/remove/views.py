from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from ublogging.models import Post


@login_required
def remove(request, postid):
    if (request.user.is_authenticated()):
        u = request.user
        p = Post.objects.get(id=postid)
        if p.user == u:
            p.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
