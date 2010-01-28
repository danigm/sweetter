from sweetter.ublogging.models import Profile
import urllib, hashlib

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
