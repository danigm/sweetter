from django.conf.urls.defaults import *
import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^sweetter/', include('sweetter.ublogging.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^login/$','django.contrib.auth.views.login',{'template_name': 'login.html'}),
    (r'^logout/$','sweetter.ublogging.views.logout'),
    (r'^join/$','sweetter.ublogging.views.join'),
    (r'^$', 'sweetter.ublogging.views.index'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
    
urlpatterns += patterns('',
    (r'^groups/', include('sweetter.contrib.groups.urls')), 
    (r'^replies/', include('sweetter.contrib.replies.urls')), 
    (r'^sweetter/vote/(?P<user_id>\d+)/$','sweetter.contrib.karma.views.vote'),
    (r'^sweetter/follow/(?P<user_id>\d+)/$','sweetter.contrib.followers.views.follow'),
   )
