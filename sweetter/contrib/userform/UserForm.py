from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import render_to_string


class UserForm:

    def __init__(self):
        pass
        
    def sidebar(self, context):
        '''    if context.user:
                form = AuthenticationForm(context['request'].POST) # A form bound to the POST data
                if form.is_valid(): # All validation rules pass
                    user = authenticate(username=form.cleaned_data.username, password=form.cleaned_data.password)
                    if user is not None and user.is_active:
                        # user logged in succesfully
                        user.login(request, user)
                        return u'Thanks'
                    else:
                        form = AuthenticationForm()
            else:
                form = AuthenticationForm()
            return render_to_string('login.html', {
                'form': form,
            })
        '''
        form = AuthenticationForm()
        s = render_to_string('loginform.html',{
            'form': form,
        })
        print s
        return s