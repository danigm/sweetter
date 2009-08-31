from django import template
from sweetter.ublogging.models import Post

register = template.Library()

@register.inclusion_tag("status/sweet.html")
def format_sweet(sweet):
    return {'post': sweet}

@register.simple_tag
def gravatar(email):    
    import urllib, hashlib

    # Set your variables here
    size = 40

    # construct the url
    gravatar_url = "http://www.gravatar.com/avatar.php?"
    gravatar_url += urllib.urlencode({'gravatar_id':hashlib.md5(email.lower()).hexdigest(), 'size':str(size)})
    return gravatar_url 
