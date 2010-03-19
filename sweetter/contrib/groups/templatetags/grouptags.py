from django import template

import ublogging
from contrib.groups.models import Group


register = template.Library()

@register.inclusion_tag("group.html")
def format_group(group):
    return {'group': group}
