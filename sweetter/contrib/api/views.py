from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.http import HttpResponse

from sweetter.ublogging.models import Post
from sweetter.ublogging import uapi
from sweetter.contrib.replies.views import get_replies

from httpauth import http_auth
from jsonize import jsonize_post

def user_timeline(request, username):
    posts = uapi.user_timeline(username, paginated=False)[:20]
    posts = [jsonize_post(i) for i in posts]
    return HttpResponse(json.dumps(posts),
            mimetype='application/json')


@http_auth
def auth_user_timeline(request):
    return user_timeline(request, request.user.username)


@http_auth
def replies(request):
    posts = get_replies(request)[:20]
    posts = [jsonize_post(i) for i in posts]
    return HttpResponse(json.dumps(posts),
            mimetype='application/json')


def friends_timeline(request, username):
    posts = uapi.friends_timeline(username)[:20]
    posts = [jsonize_post(i) for i in posts]
    return HttpResponse(json.dumps(posts),
            mimetype='application/json')


@http_auth
def auth_friends_timeline(request):
    return friends_timeline(request, request.user.username)


def public_timeline(request):
    posts = uapi.public_timeline(paginated=False)[:20]
    posts = [jsonize_post(i) for i in posts]
    return HttpResponse(json.dumps(posts),
            mimetype='application/json')


def show(request, id):
    post = jsonize_post(Post.objects.get(id=id))
    return HttpResponse(json.dumps(post),
            mimetype='application/json')


@http_auth
def update(request):
    user = request.user
    status = request.POST['status']
    post = uapi.new_post(user, status)
    return HttpResponse(json.dumps(jsonize_post(post)),
            mimetype='application/json')


@http_auth
def destroy(request, id):
    user = request.user

    p = Post.objects.filter(id=id)
    if p and p[0].user == user:
        p[0].delete()
        response = jsonize_post(p[0])
    else:
        rq = reverse(destroy, kwargs={'id':id})
        response = dict(request=rq, error="That's not yours.")
    
    return HttpResponse(json.dumps(response), mimetype='application/json')
