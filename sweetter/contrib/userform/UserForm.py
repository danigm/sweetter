from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import render_to_string
from sweetter.ublogging.models import Post
from django.core.urlresolvers import reverse

import re

class UserForm:

    def __init__(self):
        pass
        
    def sidebar(self, context):
        if context['perms'].user and not context['perms'].user.is_authenticated():
            form = AuthenticationForm(context['request'].POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                user = authenticate(username=form.cleaned_data.username, password=form.cleaned_data.password)
                if user is not None and user.is_active:
                    # user logged in succesfully
                    user.login(request, user)
                    context['user'] = user
                    return u'Thanks'
                else:
                    form = AuthenticationForm()
            else:
                form = AuthenticationForm()
            return render_to_string('loginform.html', {
                    'form': form,
                }, context_instance=context)
        else:
            return render_to_string('loggedin.html', {
                    'user':context['perms'].user
                }, context_instance=context)
                
    def tools(self, context, post):
        return ''

    def parse(self, value):
        regex = re.compile("[:punct:]*(@[A-Za-z_\-\d]*)[:punct:]*")
        matches = re.finditer(regex, value)
        if matches:
            for match in matches:
                # TODO: Fix this.
                #url = reverse('sweetter.ublogging.views.user', kwargs={'user': value[match.start() + 1:match.end()] })
                url = '/sweetter/user/' + value[match.start() + 1:match.end()]
                text = match.expand('<a href=\"'+url+'">\\1</a>')
                value = value.replace(value[match.start():match.end()], text)
        return value
        
    def post_list(self, value, request, user_name):
        return value

    def posting(self, request):
        return False
    
    def posted(self, request, post):
        pass
