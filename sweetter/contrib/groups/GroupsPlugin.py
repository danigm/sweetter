from django.template.loader import render_to_string
from sweetter.contrib.groups.models import Group
from sweetter.ublogging.api import Plugin

class GroupHooks(Plugin):
    def sidebar(self, context):
        if context['perms'].user and not context['perms'].user.is_authenticated():
            return ''
        else:
            user = context['perms'].user       
            return render_to_string('groupsidebar.html', {
                    'group_list': Group.objects.filter(users__user=user),
                }, context_instance=context)
