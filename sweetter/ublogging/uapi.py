import datetime

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q

from ublogging.models import Post, User
import ublogging


class Request_moc:

    def __init__(self, user):
        self.user = user
        self.GET = {'page': '1'}


def new_post(user, text, request=None):
    if not request:
        request = Request_moc(user)

    post = Post(text=text, user=user, pub_date=datetime.datetime.now())

    intercepted = False

    # hook for pluggins for intercepting messages. This can cancel posting them.
    for p in ublogging.plugins:
        if not intercepted:
            intercepted = p.posting(request, post)

    if not intercepted:
        post.save()
        for p in ublogging.plugins:
            p.posted(request, post)
    else:
        post = None

    return post


def public_timeline(request=None, paginated=True):
    if not request:
        request = Request_moc(None)

    latest_post_list = Post.objects.all().order_by('-pub_date')
    if paginated:
        latest_post_list = paginate_list(request, latest_post_list)

    return latest_post_list


def user_timeline(user_name, request=None, paginated=True):
    if not request:
        request = Request_moc(None)

    u = User.objects.get(username=user_name)
    q = Q(user=u)
    return show_statuses(request, q, paginated)


def own_timeline(request, paginated=True):
    if (request.user.is_authenticated()):
        q = Q(user=request.user)
        for p in ublogging.plugins:
            q = p.post_list(q, request, request.user.username)
        return show_statuses(request, q, paginated)
    else:
        raise Exception("Not authenticated")


def friends_timeline(user_name):
    u = User.objects.get(username=user_name)
    request = Request_moc(u)
    q = Q(user=u)
    for p in ublogging.plugins:
        q = p.post_list(q, request, u.username)
    return show_statuses(request, q, paginated=False)


def show_statuses(request, query, paginated=True):
    latest_post_list = Post.objects.filter(query).order_by('-pub_date')
    if paginated:
        latest_post_list = paginate_list(request, latest_post_list)

    return latest_post_list


def paginate_list(request, post_list, page=0):
    paginator = Paginator(post_list, 10)

    if not page:
        page = int(request.GET.get('page', '1'))

    try:
        post_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        post_list = paginator.page(paginator.num_pages)

    return post_list
