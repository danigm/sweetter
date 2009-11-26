from django.conf.urls.defaults import *

urlpatterns = patterns('sweetter.ublogging.views',
    (r'^$', 'index'),
    (r'public_timeline', 'public_timeline'),
	(r'status/new', 'new'),
    (r'user/(?P<user_name>.*)$','user'),	
    (r'refresh/(\d+)$', 'refresh_index'),
    (r'validate/(\w+)$', 'validate'),
    (r'profile','profile'),	
    (r'renewapikey','renewapikey'),	
)
