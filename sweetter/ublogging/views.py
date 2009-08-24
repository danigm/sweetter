from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from sweetter.ublogging.models import Post, User
import datetime

def index(request):
    latest_post_list = Post.objects.all().order_by('-pub_date')[:10]
    return render_to_response('status/index.html', {'latest_post_list': latest_post_list})

def new(request):
    text = request.POST['text']
    post = Post(text=text, userid = User.objects.all()[0], pub_date = datetime.datetime.now())
    post.save()
    return HttpResponseRedirect(reverse('sweetter.ublogging.views.index'))

