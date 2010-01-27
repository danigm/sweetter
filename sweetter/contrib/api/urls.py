from django.conf.urls.defaults import *

urlpatterns = patterns('sweetter.contrib.api.views',
    (r'statuses/user_timeline/(?P<username>\w+).json', 'user_timeline'),
    (r'statuses/friends_timeline/(?P<username>\w+).json', 'friends_timeline'),
    (r'statuses/public_timeline.json', 'public_timeline'),
    (r'statuses/show/(?P<id>\d+).json', 'show'),
)
