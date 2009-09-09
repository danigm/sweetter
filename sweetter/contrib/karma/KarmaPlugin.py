from decimal import Decimal
from sweetter.contrib.karma.models import Karma
from django.template.loader import render_to_string

class KarmaCount:      
    def __init__(self):
        pass
        
    def sidebar(self, context):
        if context['user'] and not context['user'].is_authenticated():
            return ''
        else:
            try:
                k = Karma.objects.get(user=context['user'])
            except:
                k=Karma(user=context['user'],value=0)
                k.save()
            return render_to_string('karmasidebar.html', { 'karma': k }, context_instance=context)
                
    def tools(self, context, post):
        if post.user.username == context['user'].username or not context['user'].is_authenticated():
            show = None
        else:
            show = 1
        try:
            k = Karma.objects.get(user = post.user)
        except:
            k = Karma(user = post.user, value=0)
        return render_to_string('karmatool.html', { 'karma': k, 'user':post.user, 'showvotes':show }, context_instance=context)
        
    def parse(self, value):
        return value
