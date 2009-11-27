from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import logout as djlogout
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.template import RequestContext
from sweetter.ublogging.models import RegisterUserForm
from sweetter import ublogging
from sweetter.ublogging.models import Post, User, Profile
from sweetter.ublogging import api
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from sweetter import flash
import datetime

import register
join = register.join
validate = register.validate

from profile import profile
from profile import renewapikey

def public_timeline(request):
    latest_post_list = Post.objects.all().order_by('-pub_date')
    latest_post_list = paginate_list(request, latest_post_list)
    
    return render_to_response('status/index.html', {
            'latest_post_list': latest_post_list,
            'viewing': "public",
        }, context_instance=RequestContext(request))

def index(request, only_list=False):
    if (request.user.is_authenticated()):
        q = Q(user = request.user)
        for p in ublogging.plugins:
            q = p.post_list(q, request, request.user.username)
        return show_statuses(request, q, only_list=only_list)
    else:
        return public_timeline(request)

def user(request, user_name, only_list=False):
    u = User.objects.get(username = user_name)
    q = Q(user = u)
    return show_statuses(request, q, u, only_list=only_list)

def paginate_list(request, post_list, page=0):
    paginator = Paginator(post_list, 10) 

    if not page:
        page = int(request.GET.get('page', '1'))
    
    try:
        post_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        post_list = paginator.page(paginator.num_pages)

    return post_list

def show_statuses(request, query, user=None, only_list=False):
    latest_post_list = Post.objects.filter(query).order_by('-pub_date')
    if only_list:
        return latest_post_list

    latest_post_list = paginate_list(request, latest_post_list)

    if user:
        profile = Profile.objects.get(user=user)
    else:
        profile = None
    
    return render_to_response('status/index.html', {
            'latest_post_list': latest_post_list,
            'viewing_user': user,
            'viewing_profile': profile,
        }, context_instance=RequestContext(request))

@login_required
def new(request):
    text = request.POST['text']
    new_post(request.user, text, request)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    #return HttpResponseRedirect(reverse('sweetter.ublogging.views.index'))

def new_post(user, text, request):
    post = Post(text=text, user=user, pub_date=datetime.datetime.now())
    
    intercepted = False
    
    # hook for pluggins for intercepting messages. This can cancel posting them.
    for p in ublogging.plugins:
        if not intercepted:
            intercepted = p.posting(request)
    
    if not intercepted:
        post.save()
        for p in ublogging.plugins:
            p.posted(request, post)

@login_required
def logout(request):
    djlogout(request)
    return HttpResponseRedirect(reverse('sweetter.ublogging.views.index'))

from django.core import serializers

def refresh_public(request, lastid):
    latest_post_list = Post.objects.all().order_by('-pub_date')
    return HttpResponse("")

import re
def refresh_index(request, lastid, pagenumber):
    url = request.META['HTTP_REFERER']
    usere = r'(.*)/user/(?P<username>[^\?\/]*)'
    publice = r'(.*)/public_timeline'

    user_timeline = re.match(usere, url)
    public_timeline = re.match(publice, url)
    if user_timeline:
        latest_post_list = user(request, user_timeline.group('username'), only_list=True)
    elif public_timeline:
        latest_post_list = Post.objects.all().order_by('-pub_date')
    else:
        latest_post_list = index(request, only_list=True)

    latest_post_list = latest_post_list.filter(pk__gt=lastid)

    if latest_post_list:
        latest_post_list = paginate_list(request, latest_post_list, int(pagenumber))
        return render_to_response('status/refresh.html',
                                {'latest_post_list': latest_post_list },
                                context_instance=RequestContext(request))
    else:
        return HttpResponse("")

