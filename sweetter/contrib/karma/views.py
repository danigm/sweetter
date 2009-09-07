from sweetter.contrib.karma.models import Karma
from sweetter.ublogging.models import Post, User

def up(request):
    try:
        k=Karma.objects.get(user=context['user'])
        k.value = k.value+1
        k.save()
    except
        return ''