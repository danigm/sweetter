from django.conf.urls.defaults import *

urlpatterns = patterns('sweetter.contrib.recoverpw.views',
    (r'recover/$', 'index'),
    (r'validate/(\w+)$', 'validate'),
)

