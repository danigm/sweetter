from decimal import Decimal
from sweetter.contrib.followers.models import Follower
from django.template.loader import render_to_string

class FollowingList:      
    def __init__(self):
        pass
        
    def sidebar(self, context):
        if context['user'] and not context['user'].is_authenticated():
            return ''
        else:
            try:
                f_list = Follower.objects.filter(follower = context['user'])
            except:
                return ''
            return render_to_string('following.html', { 'following': f_list }, context_instance=context)
                
    def tools(self, context, post):
        return ''
        
    def parse(self, value):
        return value

class FollowerList:      
    def __init__(self):
        pass
        
    def sidebar(self, context):
        if context['user'] and not context['user'].is_authenticated():
            return ''
        else:
            try:
                f_list = Follower.objects.filter(user = context['user'])
            except:
                return ''
            return render_to_string('follower.html', { 'followers': f_list }, context_instance=context)
                
    def tools(self, context, post):
        return ''
        
    def parse(self, value):
        return value      