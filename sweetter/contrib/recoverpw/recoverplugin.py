import re

from django.core.urlresolvers import reverse

from ublogging.api import Plugin


class Recover(Plugin):

    def sidebar(self, context):
        if not context.get('viewing_user', '') and not context['perms'].user.is_authenticated():
            return '<a href="'+reverse('contrib.recoverpw.views.index')+'">Password recovery</a>'
        else:
            return ""
