from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from os import path

BASEDIR = path.dirname(path.abspath(__file__))

urlpatterns = patterns('',
    url(r'^$', 'account_linking.views.home', name='home'),
    url(r'^openid$', 'account_linking.views.openid', name='openid'),
    url(r'^rp$', 'account_linking.views.rp', name='rp'),
    url(r'^authz_cb$', 'account_linking.views.authz_cb', name='authz_cb'),
    url(r'^logout$', 'account_linking.views.logout', name='logout'),

    # Examples:
    # url(r'^access_web/', include('access_web.foo.urls')),
    #url(r'^nss_list/', include('nss_list.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

#    url(r'^shib/', include('shibboleth.urls', namespace='shibboleth')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': path.join(BASEDIR, "static")})
)
