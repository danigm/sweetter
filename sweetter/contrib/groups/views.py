from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from sweetter.ublogging.models import Post, User
from sweetter.contrib.groups.models import Group
import datetime

def index(request):
    groups_list = Group.objects.all()
    return render_to_response('allgroups.html', {
            'object_list': groups_list
        }, context_instance=RequestContext(request))