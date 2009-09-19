from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from sweetter.ublogging.models import Post, User, Profile
from sweetter.contrib.groups.models import Group
import datetime

def detail(request,object_id):
    g = Group.objects.get(id=object_id)
    if g.users.filter(user=request.user):
        join_message = u'Leave'
    else:
        join_message = u'Join'
    return render_to_response('groups/detail.html', {
            'object': g, 'join_message':join_message
        }, context_instance=RequestContext(request))
        
def join(request,group_name):
    g = Group.objects.get(name=group_name)
    try:
        u = g.users.get(user=request.user)
        g.users.remove(u)
        join_message = u'Join'
    except:
        p = Profile.objects.get(user=request.user)
        g.users.add(p)
        join_message = u'Leave'
    g.save()
    return render_to_response('groups/detail.html', {
            'object': g, 'join_message':join_message
        }, context_instance=RequestContext(request))
        