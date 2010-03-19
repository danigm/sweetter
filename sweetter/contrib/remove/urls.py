from django.conf.urls.defaults import *

urlpatterns = patterns('contrib.remove.views',
    (r'remove/(\d+)$', 'remove'),
)
