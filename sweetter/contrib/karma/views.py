from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from sweetter.contrib.karma.models import Karma
from sweetter.ublogging.models import Post, User
from django.contrib.auth.decorators import login_required

@login_required
def vote(request,user_id):
    u=User.objects.get(id=user_id)
    sum = float(request.POST['vote'])
    try:
        k=Karma.objects.get(user=u)
    except:
        k=Karma(user=u,value=0)
    k.value = k.value+(sum*0.1)
    k.save()
    return HttpResponseRedirect(reverse('sweetter.ublogging.views.index'))
