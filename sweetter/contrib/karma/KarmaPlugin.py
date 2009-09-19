from decimal import Decimal
from sweetter.ublogging.models import Post, User
from sweetter.contrib.karma.models import Karma
from django.template.loader import render_to_string
from django.db.models import Q

class KarmaCount:      
    def __init__(self):
        pass
        
    def sidebar(self, context):
        if context['perms'].user and not context['perms'].user.is_authenticated():
            return ''
        else:
            try:
                k = Karma.objects.get(user=context['perms'].user)
            except:
                k=Karma(user=context['perms'].user,value=0)
                k.save()
            return render_to_string('karmasidebar.html', { 'karma': k }, context_instance=context)
                
    def tools(self, context, post):
        if not context['perms'].user.is_authenticated() or post.user.username == context['perms'].user.username:
            return ''
        try:
            k = Karma.objects.get(user = post.user)
        except:
            k = Karma(user = post.user, value=0)
        return render_to_string('karmatool.html', { 'karma': k, 'user':post.user }, context_instance=context)
        
    def parse(self, value):
        return value
        
    def post_list(self, value, request, user_name):
        return value
