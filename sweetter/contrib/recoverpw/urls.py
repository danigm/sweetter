from django.conf.urls.defaults import *

urlpatterns = patterns('contrib.recoverpw.views',
    (r'recover/$', 'index'),
    (r'validate/(\w+)$', 'validate'),
)

