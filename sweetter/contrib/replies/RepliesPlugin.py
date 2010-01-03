from sweetter.ublogging.api import Plugin
from django.template.loader import render_to_string
from sweetter.ublogging.models import Post
from django.db.models import Q
from django.core.urlresolvers import reverse

import re

class RepliesPlugin(Plugin):
    def __init__(self):
        self.script = '''
<script>
    $(".reply").click(function(){
        username = $(this).attr("title");
        $("#text")[0].value += "@" + username;
        $("#text").focus();
        return false;
    });
</script>
'''
    
    def parse(self, value):
        regex = re.compile("[:punct:]*(@[A-Za-z_\-\d]*)[:punct:]*")
        matches = re.findall(regex, value)
        if matches:
            dict = { }
            for match in matches:
                url = reverse('sweetter.ublogging.views.user', args= [match[1:]])
                text = '<a href="'+url+'">'+match+'</a>'
                dict[match] = text
            for key in dict:                
                value = value.replace(key, dict[key])
        return value
    
    def post_list(self, value, request, user_name):      
        return value | Q(text__contains = "@"+user_name)
    
    def sidebar(self, context):
        if context['perms'].user and not context['perms'].user.is_authenticated():
            return ''
        else:
            user = context['perms'].user
            replies = str(Post.objects.filter(text__contains="@"+user.username).count())
            posts = str(Post.objects.filter(user=user).count())
            url = reverse('sweetter.contrib.replies.views.replies')
            return self.script +\
                    '<a href="'+url+'">Replies</a>: '+replies+\
                    " | Sweets: "+posts

    def tools(self, context, post):
        if not context['perms'].user.is_authenticated() or (post.user.username == context['perms'].user.username):
            return ''

        return render_to_string('reply.html', {'user': post.user}, context_instance=context)
