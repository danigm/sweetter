from django.conf.urls.defaults import *

urlpatterns = patterns('sweetter.contrib.replies.views',
    (r'^$', 'replies'),
    (r'^(?P<user_name>.*)/$', 'replies_username'),
)
