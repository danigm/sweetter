from django import template
from sweetter import ublogging
from sweetter.contrib.groups.models import Group

register = template.Library()

@register.inclusion_tag("group.html")
def format_group(group):
    return {'group': group}