from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import render_to_string
from sweetter.ublogging.models import Post

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
        return value