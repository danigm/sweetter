from django.core.urlresolvers import reverse
from sweetter.ublogging.api import Plugin

import re
  
class Recover(Plugin):
    def sidebar(self, context):
        if not context.get('viewing_user','') and not context['perms'].user.is_authenticated():
            return '<a href="'+reverse('sweetter.contrib.recoverpw.views.index')+'">Password recovery</a>'
        else:
            return ""

