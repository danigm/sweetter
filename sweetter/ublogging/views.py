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

def index(request):
    if (request.user.is_authenticated()):
        q = Q(user = request.user)
        for p in ublogging.plugins:
            q = p.post_list(q, request, request.user.username)
        return show_statuses(request, q)
    else:
        return public_timeline(request)

def user(request, user_name):
    u = User.objects.get(username = user_name)
    q = Q(user = u)
    return show_statuses(request, q, u)

def show_statuses(request, query, user=None):
    latest_post_list = Post.objects.filter(query).order_by('-pub_date')
    paginator = Paginator(latest_post_list, 10) 

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        latest_post_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        latest_post_list = paginator.page(paginator.num_pages)

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

def refresh_index(request, lastid):
    lastid = int(lastid)
    if (request.user.is_authenticated()):
        q = Q(user = request.user)
        for p in ublogging.plugins:
            q = p.post_list(q, request, request.user.username)

        latest_post_list = Post.objects.filter(q).filter(pk__gt=lastid).order_by('-pub_date')
        paginator = Paginator(latest_post_list, 10)
        latest_post_list = paginator.page(1).object_list
        data = serializers.serialize("json", latest_post_list)
        return HttpResponse(data)
    else:
        return HttpResponse("")

