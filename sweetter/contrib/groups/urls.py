from django.conf.urls.defaults import *

urlpatterns = patterns('sweetter.contrib.groups.views',
    (r'^$', 'index'),
    (r'index', 'index'),
)
