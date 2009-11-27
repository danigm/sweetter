from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from sweetter.ublogging.models import Post, User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from sweetter.ublogging.views import paginate_list

def get_replies(request, user_name=None):
    if user_name is None:
        user_name = request.user.username
    q = Q(text__contains = "@"+user_name)
    latest_post_list = Post.objects.filter(q).order_by('-pub_date')

    return latest_post_list

def replies(request, user_name=None):
    latest_post_list = get_replies(request, user_name)
    latest_post_list = paginate_list(request, latest_post_list)
    return render_to_response('status/index.html', {
            'latest_post_list': latest_post_list,
            'refresh_uri': '/replies/refresh',
        }, context_instance=RequestContext(request))

import re
def refresh(request, lastid, pagenumber):
    url = request.META['HTTP_REFERER']
    usere = r'(.*)/replies/(?P<username>[^\?\/]*)'

    user_replies = re.match(usere, url)
    if user_replies:
        latest_post_list = get_replies(request, user_replies.group('username'))
    else:
        latest_post_list = get_replies(request)

    latest_post_list = latest_post_list.filter(pk__gt=lastid)

    if latest_post_list:
        latest_post_list = paginate_list(request, latest_post_list, int(pagenumber))
        return render_to_response('status/refresh.html',
                                {'latest_post_list': latest_post_list },
                                context_instance=RequestContext(request))
    else:
        return HttpResponse("")

def replies_username(request, user_name):
    return replies(request, user_name)
