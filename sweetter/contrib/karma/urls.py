from django.conf.urls.defaults import *

urlpatterns = patterns('contrib.karma.views',
    (r'^$', 'index'),
    (r'index', 'index'),
)
