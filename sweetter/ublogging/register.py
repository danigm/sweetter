from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from ublogging.models import Profile, User
from ublogging.models import RegisterUserForm
import flash


def send_confirmation(user):
    subject = "sweetter 3.0 registry confirmation"
    profile = Profile.objects.get(user=user)
    from_email = settings.MSG_FROM
    vars = {'username': user.username, 'apikey': profile.apikey}
    message = settings.CONFIRMATION_MSG % vars

    to_email = user.email
    send_mail(subject, message, from_email, [to_email], fail_silently=False)


def join(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            user.is_active = False
            user.save()

            send_confirmation(user)

            flash.set_flash(request, "Thanks for register, you'll receive a confirmation email")
            form = RegisterUserForm()
            return render_to_response('join.html', {
                'form': form,
            }, context_instance=RequestContext(request))
        else:
            flash.set_flash(request, "Validation error", "error")
            return render_to_response('join.html', {
                'form': form
            }, context_instance=RequestContext(request))
    else:
        form = RegisterUserForm()
        return render_to_response('join.html', {
            'form': form,
        }, context_instance=RequestContext(request))


def validate(request, apikey):
    try:
        profile = Profile.objects.get(apikey=apikey)
        profile.user.is_active = True
        profile.user.save()
        flash.set_flash(request, "User validated, now you can loggin")
    except:
        flash.set_flash(request, "Invalid apikey", "error")

    return HttpResponseRedirect(reverse('ublogging.views.index'))


def adduser(username, password, email):
    u = User(username=username, email=email)
    u.set_password(password)
    u.is_active = True
    u.save()

    profile, new = Profile.objects.get_or_create(user=u)
    profile.save()

    return u
