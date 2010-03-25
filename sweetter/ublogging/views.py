import re

from django.contrib.auth import logout as djlogout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext

from ublogging import api
from ublogging import uapi
from ublogging.models import Post, User, Profile
from ublogging.models import RegisterUserForm
from ublogging.profile import profile, renewapikey
from ublogging.register import join, validate
from ublogging.uapi import paginate_list
import flash
import ublogging


def sweet(request, sweetid):
    sweetid=int(sweetid)
    sweet = get_object_or_404(Post, id=sweetid)
    user = sweet.user
    profile = Profile.objects.get(user=user)
    return render_to_response('status/index.html', {
            'latest_post_list': None,
            'sweet': sweet,
            'viewing_user': user,
            'viewing_profile': profile,
        }, context_instance=RequestContext(request))


def public_timeline(request):
    latest_post_list = uapi.public_timeline(request)

    return render_to_response('status/index.html', {
            'latest_post_list': latest_post_list,
            'feedurl': reverse('django.contrib.syndication.views.feed', kwargs={'url': 'public'}),
            'viewing': "public",
        }, context_instance=RequestContext(request))


def index(request):
    try:
        latest_post_list = uapi.own_timeline(request)
    except:
        return public_timeline(request)

    return show_statuses(request, latest_post_list)


def user(request, user_name):
    u = get_object_or_404(User, username=user_name)
    latest_post_list = uapi.user_timeline(user_name, request)
    return show_statuses(request, latest_post_list, user=u)


def show_statuses(request, latest_post_list, user=None):
    if user:
        profile = Profile.objects.get(user=user)
        feedurl = reverse('django.contrib.syndication.views.feed', kwargs={'url': 'user/%s' % user.username})
    else:
        feedurl = reverse('django.contrib.syndication.views.feed', kwargs={'url': 'user/%s' % request.user.username})
        profile = None

    return render_to_response('status/index.html', {
            'latest_post_list': latest_post_list,
            'viewing_user': user,
            'viewing_profile': profile,
            'feedurl': feedurl,
        }, context_instance=RequestContext(request))


@login_required
def new(request):
    text = request.POST['text']
    uapi.new_post(request.user, text, request)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    #return HttpResponseRedirect(reverse('ublogging.views.index'))


@login_required
def logout(request):
    djlogout(request)
    return HttpResponseRedirect(reverse('ublogging.views.index'))


def refresh_index(request, lastid, pagenumber):
    url = request.META['HTTP_REFERER']
    usere = r'(.*)/user/(?P<username>[^\?\/]*)'
    publice = r'(.*)/public_timeline'
    lastid=int(lastid)

    user_timeline = re.match(usere, url)
    public_timeline = re.match(publice, url)
    if user_timeline:
        latest_post_list = uapi.user_timeline(user_timeline.group('username'), request, paginated=False)
    elif public_timeline:
        latest_post_list = uapi.public_timeline(request, paginated=False)
    else:
        try:
            latest_post_list = uapi.own_timeline(request, paginated=False)
        except:
            latest_post_list = uapi.public_timeline(request, paginated=False)

    lastpost = Post.objects.filter(pk=lastid)[0]
    latest_post_list = latest_post_list.filter(pub_date__gt=lastpost.pub_date)

    if latest_post_list:
        latest_post_list = paginate_list(request, latest_post_list, int(pagenumber))
        return render_to_response('status/refresh.html',
                                {'latest_post_list': latest_post_list },
                                context_instance=RequestContext(request))
    else:
        return HttpResponse("")
