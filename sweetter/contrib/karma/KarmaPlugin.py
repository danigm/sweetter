from django.template.loader import render_to_string

from ublogging.api import Plugin
from contrib.karma.models import Karma


class KarmaCount(Plugin):

    def sidebar(self, context):
        if context.get('viewing_user', ''):
            user = context['viewing_user']
        else:
            user = context['perms'].user
        if user.is_authenticated():
            try:
                k = Karma.objects.get(user=user)
            except:
                k = Karma(user=user, value=0)
                k.save()
        else:
            k = False
        karma_ranking = Karma.objects.all().order_by('-value')[:5]
        return render_to_string('karmasidebar.html',
                                {'karma': k, 'karma_ranking': karma_ranking},
                                context_instance=context)

    def tools(self, context, post):
        if not context.get('viewing_user', '') and context['perms'].user and not context['perms'].user.is_authenticated():
            return ''
        try:
            k = Karma.objects.get(user=post.user)
        except:
            k = Karma(user=post.user, value=0)
        return render_to_string('karmatool.html',
                                {'karma': k, 'user': post.user},
                                context_instance=context)
