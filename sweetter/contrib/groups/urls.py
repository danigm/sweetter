from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse

from contrib.groups.models import Group

info_dict = {
    'queryset': Group.objects.all(),
}

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.list_detail.object_list',
               dict(info_dict, template_name='groups/list.html'),
               'contrib.groups.views.index'),
    url(r'^index$', 'django.views.generic.list_detail.object_list',
                    dict(info_dict, template_name='groups/list.html'),
                    'contrib.groups.views.index2'),
    url(r'^detail/(?P<object_id>\d+)/$', 'contrib.groups.views.detail'),
    url(r'^join/(?P<group_name>.*)/$', 'contrib.groups.views.join'),
    url(r'^(?P<group_name>.*)/$', 'contrib.groups.views.messages')
    )

urlpatterns += patterns('',
    url(r'^new$', 'django.views.generic.create_update.create_object',
                  dict(model= Group, login_required= True,
                       post_save_redirect=reverse('contrib.groups.views.index'),
                       template_name='groups/create.html'),
                  'contrib.groups.views.create')
    )
