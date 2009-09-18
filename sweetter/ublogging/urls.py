from django.conf.urls.defaults import *

urlpatterns = patterns('sweetter.ublogging.views',
    (r'^$', 'index'),
    (r'index', 'index'),
	(r'status/new', 'new'),
	(r'join','join'),
)
