from decimal import Decimal
from sweetter.contrib.followers.models import Follower
from django.template.loader import render_to_string
from django.db.models import Q
from sweetter.ublogging.api import Plugin

class FollowingList(Plugin):      
    def sidebar(self, context):
        if not context.get('viewing_user','') and context['perms'].user and not context['perms'].user.is_authenticated():
            return ''
        else:
            if context.get('viewing_user', ''):
                user = context['viewing_user']
            else:
                user = context['perms'].user
            try:
                f_list = Follower.objects.filter(follower=user)
            except:
                return ''
            return render_to_string('following.html', { 'following': f_list }, context_instance=context)

    def headbar(self, context):
        if not context.get('viewing_user','') or not context['perms'].user or not context['perms'].user.is_authenticated():
            return ''

        if context.get('viewing_user', '') == context['perms'].user:
            return ''

        user = context['viewing_user']
        try:
            f = Follower.objects.get(user=user, follower=context['perms'].user)
            following = True
            image = u'followno'
        except:
            following = False
            image = u'follow'
        return render_to_string('follow.html',
                {'user': user, 'image':image, 'following': following},
                context_instance=context)

class FollowerList(Plugin):      
    def sidebar(self, context):
        if not context.get('viewing_user','') and context['perms'].user and not context['perms'].user.is_authenticated():
            return ''
        else:
            if context.get('viewing_user', ''):
                user = context['viewing_user']
            else:
                user = context['perms'].user
            try:
                f_list = Follower.objects.filter(user=user)
            except:
                return ''
            return render_to_string('follower.html', { 'followers': f_list }, context_instance=context)
                
    def post_list(self, value, request, user_name):
        return value | Q(user__in = Follower.objects.filter(follower=request.user).values('user'))
