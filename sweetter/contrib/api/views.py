import urllib, hashlib
from django.http import HttpResponse
from sweetter.ublogging.models import Post, User, Profile
from sweetter.ublogging import uapi
from django.contrib.auth import authenticate

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


def update(request):
    authorization = request.META.get('HTTP_AUTHORIZATION', '')
    if not authorization:
        return basic_challenge()
    user = basic_authenticate(authorization)
    if user:
        status = request.POST['status']
        post = uapi.new_post(user, status)
        return HttpResponse(json.dumps(jsonize_post(post)),
                mimetype='application/json')
    
    return basic_challenge()


def basic_challenge(realm=None):
    if realm is None:
        realm = 'Restricted Access'
    response =  HttpResponse('Authorization Required', mimetype="text/plain")
    response['WWW-Authenticate'] = 'Basic realm="%s"' % (realm)
    response.status_code = 401
    return response


def basic_authenticate(authentication):
    # Taken from paste.auth
    (authmeth, auth) = authentication.split(' ',1)
    if 'basic' != authmeth.lower():
        return None
    auth = auth.strip().decode('base64')
    username, password = auth.split(':',1)
    return authenticate(username=username, password=password)


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
                    screen_name=user.username,
                    name=user.username,
                    profile_image_url=gravatar(user.email))

    return user_data


def gravatar(email, size=48):    
    gravatar_url = "http://www.gravatar.com/avatar.php?"
    gravatar_url += urllib.urlencode({'gravatar_id':hashlib.md5(email.lower()).hexdigest(), 'size':str(size)})
    return gravatar_url 
