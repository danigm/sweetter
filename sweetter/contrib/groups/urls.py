'''from django.conf.urls.defaults import *

urlpatterns = patterns('sweetter.contrib.groups.views',
    (r'^$', 'index'),
    (r'index', 'index'),
)
'''
from django.core.urlresolvers import reverse
from django.conf.urls.defaults import *
from sweetter.contrib.groups.models import Group

info_dict = {
    'queryset': Group.objects.all(),
}

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.list_detail.object_list', dict(info_dict, template_name='groups/list.html'),   
        'sweetter.contrib.groups.views.index'),
    url(r'^index$', 'django.views.generic.list_detail.object_list', dict(info_dict, template_name='groups/list.html'),
        'sweetter.contrib.groups.views.index2'),
    url(r'^detail/(?P<object_id>\d+)/$', 
        'django.views.generic.list_detail.object_detail', dict(info_dict, template_name='groups/detail.html'), 
        'sweetter.contrib.groups.views.detail'),
    url(r'^new$', 
        'django.views.generic.create_update.create_object', dict(model= Group, 
            login_required= True, post_save_redirect='/groups/',
            template_name='groups/create.html'),
        'sweetter.contrib.groups.views.create'
        )
    )