from decimal import Decimal
from sweetter.contrib.followers.models import Follower
from django.template.loader import render_to_string

class FollowingList:      
    def __init__(self):
        pass
        
    def sidebar(self, context):
        if context['perms'].user and not context['perms'].user.is_authenticated():
            return ''
        else:
            try:
                f_list = Follower.objects.filter(follower = context['perms'].user)
            except:
                return ''
            return render_to_string('following.html', { 'following': f_list }, context_instance=context)
                
    def tools(self, context, post):
        if not context['perms'].user.is_authenticated() or (post.user.username == context['perms'].user.username):
            return ''
        try:
            f = Follower.objects.get(user = post.user, follower = context['perms'].user)
            image = u'followno'
        except:
            image = u'follow'
        return render_to_string('follow.html', {'user': post.user, 'image':image}, context_instance=context)
        
    def parse(self, value):
        return value

class FollowerList:      
    def __init__(self):
        pass
        
    def sidebar(self, context):
        if context['perms'].user and not context['perms'].user.is_authenticated():
            return ''
        else:
            try:
                f_list = Follower.objects.filter(user = context['perms'].user)
            except:
                return ''
            return render_to_string('follower.html', { 'followers': f_list }, context_instance=context)
                
    def tools(self, context, post):
        return ''
        
    def parse(self, value):
        return value
