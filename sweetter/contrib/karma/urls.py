from django.conf.urls.defaults import *

urlpatterns = patterns('sweetter.contrib.karma.views',
    (r'^$', 'index'),
    (r'index', 'index'),
)
