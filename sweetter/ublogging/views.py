from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from sweetter.ublogging.models import Post, User
import datetime

def index(request):
    latest_post_list = Post.objects.all().order_by('-pub_date')[:10]
    return render_to_response('status/index.html', {
            'latest_post_list': latest_post_list
        }, context_instance=RequestContext(request))

def new(request):
    text = request.POST['text']
    post = Post(text=text, userid = User.objects.all()[0], pub_date = datetime.datetime.now())
    post.save()
    return HttpResponseRedirect(reverse('sweetter.ublogging.views.index'))

def join(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            errormessage = "Gracias por registrarte"
            form = UserCreationForm()
            return render_to_response('join.html', {
                'error_message': errormessage,
                'form': form,
            }, context_instance=RequestContext(request))
        else:
            return render_to_response('join.html', {
                'error_message': "Error de validacion",
                'form': form
            }, context_instance=RequestContext(request))
    else:
        form = UserCreationForm()
        return render_to_response('join.html', {
            'form': form,
        }, context_instance=RequestContext(request))
    