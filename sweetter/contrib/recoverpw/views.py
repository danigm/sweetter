import random
import string

from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from contrib.recoverpw.models import Recover
from ublogging.models import User
import flash


def index(request):
    if request.method == 'GET':
        return render_to_response("recover.html", {},
        context_instance=RequestContext(request))

    username = request.POST['username']

    u = User.objects.filter(username=username)
    if len(u):
        u = u[0]
    else:
        return HttpResponseRedirect(reverse('ublogging.views.index'))

    try:
        r = Recover.objects.filter(user=u)[0]
        r.regen_key()
    except:
        r = Recover(user=u)

    r.save()

    mail = u.email
    key = r.key

    subject = "sweetter 3.0 password recovery"
    from_email = settings.MSG_FROM
    vars = {'username': u.username, 'key': key}
    message = settings.RECOVERY_MSG % vars

    to_email = mail
    send_mail(subject, message, from_email, [to_email], fail_silently=False)

    flash.set_flash(request, "Recovery proccess starts, you'll receive a confirmation email")
    return HttpResponseRedirect(reverse('ublogging.views.index'))


def validate(request, key):
    k = Recover.objects.filter(key=key)
    if len(k):
        k = k[0]
    else:
        flash.set_flash(request, "wrong recovery key", "error")
        return HttpResponseRedirect(reverse('ublogging.views.index'))

    u = k.user
    chars = string.letters + string.digits
    newp = ''.join([random.choice(chars) for i in range(11)])

    u.set_password(newp)
    u.save()

    k.delete()

    flash.set_flash(request, "'%s' your new password is '%s', login and change it." % (u.username, newp))
    return HttpResponseRedirect(reverse('ublogging.views.index'))
