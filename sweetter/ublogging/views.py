from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.template import RequestContext
from sweetter.ublogging.models import RegisterUserForm
from sweetter import ublogging
from sweetter.ublogging.models import Post, User
from django.db.models import Q
import datetime

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
    return show_statuses(request, q)

def show_statuses(request, query):
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
    
    return render_to_response('status/index.html', {
            'latest_post_list': latest_post_list
        }, context_instance=RequestContext(request))

def new(request):
    text = request.POST['text']
    post = Post(text=text, user = request.user, pub_date = datetime.datetime.now())
    
    intercepted = False
    
    # hook for pluggins for intercepting messages. This can cancel posting them.
    for p in ublogging.plugins:
        if not intercepted:
            intercepted = p.posting(request)
    
    if not intercepted:
        post.save()
        for p in ublogging.plugins:
            p.posted(request, post)
        
    return HttpResponseRedirect(reverse('sweetter.ublogging.views.index'))

def join(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            errormessage = "Gracias por registrarte"
            form = RegisterUserForm()
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
        form = RegisterUserForm()
        return render_to_response('join.html', {
            'form': form,
        }, context_instance=RequestContext(request))
    
