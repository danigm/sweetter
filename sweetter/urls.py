from django.conf.urls.defaults import *
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^sweetter/', include('sweetter.ublogging.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^sweetter/login/$','django.contrib.auth.views.login',{'template_name': 'login.html'}),
    (r'^sweetter/logout/$','django.contrib.auth.views.logout'),
    (r'^sweetter/vote/(?P<user_id>\d+)/$','sweetter.contrib.karma.views.vote'),
    (r'^sweetter/follow/(?P<user_id>\d+)/$','sweetter.contrib.followers.views.follow'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
    
urlpatterns += patterns('',
    (r'^groups/', include('sweetter.contrib.groups.urls')),
   )