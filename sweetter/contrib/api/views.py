import urllib, hashlib
from django.http import HttpResponse
from sweetter.ublogging.models import Post, User, Profile
from sweetter.ublogging import uapi

from django.utils import simplejson as json

def user_timeline(request, username):
    posts = uapi.user_timeline(username, paginated=False)[:20]
    posts = [jsonize_post(i) for i in posts]
    return HttpResponse(json.dumps(posts),
            mimetype='application/json')


def friends_timeline(request, username):
    posts = uapi.friends_timeline(username)[:20]
    posts = [jsonize_post(i) for i in posts]
    return HttpResponse(json.dumps(posts),
            mimetype='application/json')


def public_timeline(request):
    posts = uapi.public_timeline(paginated=False)[:20]
    posts = [jsonize_post(i) for i in posts]
    return HttpResponse(json.dumps(posts),
            mimetype='application/json')


def show(request, id):
    post = jsonize_post(Post.objects.get(id=id))
    return HttpResponse(json.dumps(post),
            mimetype='application/json')


def jsonize_post(post):
    user = jsonize_user(post.user)

    post_data = dict(user=user,
                    created_at=post.pub_date.ctime(),
                    id=post.id,
                    text=post.text)
    
    return post_data

def jsonize_user(user):
    p = Profile.objects.get(user=user)
    user_data = dict(url=p.url,
                    location=p.location,
                    name=user.username,
                    profile_image_url=gravatar(user.email))

    return user_data

def gravatar(email, size=48):    
    gravatar_url = "http://www.gravatar.com/avatar.php?"
    gravatar_url += urllib.urlencode({'gravatar_id':hashlib.md5(email.lower()).hexdigest(), 'size':str(size)})
    return gravatar_url 
