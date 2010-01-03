from sweetter.ublogging.api import Plugin
from django.core.urlresolvers import reverse

import re

class RemovePlugin(Plugin):
    def tools(self, context, post):
        if not context['perms'].user.is_authenticated() or\
               (post.user.username != context['perms'].user.username):
            return ''

        url = reverse('sweetter.contrib.remove.views.remove', args=[post.id])

        link = '''<div
            style="background: transparent url('/static/remove.png') no-repeat; padding-left: 16px;">
            <a href="%s">delete</a></div>'''

        return link % url
