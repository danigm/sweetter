from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.utils import simplejson as json

def basic_challenge(realm=None):
    if realm is None:
        realm = 'Restricted Access'
    error = dict(request='', error="Could not authenticate you.")
    response = HttpResponse(json.dumps(error), mimetype='application/json')
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


def http_auth(function, *args, **kwargs):
    def decorator(request, *args, **kwargs):
        authorization = request.META.get('HTTP_AUTHORIZATION', '')
        if not authorization:
            return basic_challenge()
        user = basic_authenticate(authorization)
        if user:
            request.user = user
            return function(request, *args, **kwargs)

        return basic_challenge()
        
    
    decorator.__doc__ = function.__doc__
    decorator.__name__ = function.__name__
    decorator.__dict__.update(function.__dict__)

    return decorator
