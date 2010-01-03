from django.conf.urls.defaults import *

urlpatterns = patterns('sweetter.contrib.remove.views',
    (r'remove/(\d+)$', 'remove'),
)
