from decimal import Decimal
from sweetter.ublogging.models import Post, User
from sweetter.contrib.karma.models import Karma
from django.template.loader import render_to_string
from django.db.models import Q
from sweetter.ublogging.api import Plugin

class KarmaCount(Plugin):      
    def sidebar(self, context):
        if context['perms'].user and not context['perms'].user.is_authenticated():
            return ''
        else:
            if context.get('viewing_user', ''):
                user = context['viewing_user']
            else:
                user = context['perms'].user
            try:
                k = Karma.objects.get(user=user)
            except:
                k=Karma(user=user,value=0)
                k.save()
            karma_ranking = Karma.objects.all().order_by('-value')[:5]
            return render_to_string('karmasidebar.html', 
                { 'karma': k, 'karma_ranking': karma_ranking}, context_instance=context)
                
    def tools(self, context, post):
        if not context['perms'].user.is_authenticated() or post.user.username == context['perms'].user.username:
            return ''
        try:
            k = Karma.objects.get(user = post.user)
        except:
            k = Karma(user = post.user, value=0)
        return render_to_string('karmatool.html', { 'karma': k, 'user':post.user }, context_instance=context)
