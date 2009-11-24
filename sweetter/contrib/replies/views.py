from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from sweetter.contrib.karma.models import Karma
from sweetter.ublogging.models import Post, User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required

@login_required
def replies(request, user_name = None):
    if user_name is None:
        user_name = request.user.username
    q = Q(text__contains = "@"+user_name)
    latest_post_list = Post.objects.filter(q).order_by('-pub_date')
    paginator = Paginator(latest_post_list, 10) 

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        latest_post_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        latest_post_list = paginator.page(paginator.num_pages)
 
    return render_to_response('status/index.html', {
            'latest_post_list': latest_post_list
        }, context_instance=RequestContext(request))
        
def replies_username(request, user_name):
    return replies(request, user_name)
