from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from os import path

BASEDIR = path.dirname(path.abspath(__file__))

urlpatterns = patterns('',
    # URLS for OpenId authentication
    url(r'^openid$', 'django_rp.oidc_django.views.openid', name='openid'),
    url(r'^rp$', 'django_rp.oidc_django.views.rp', name='rp'),
    url(r'^authz_cb$', 'django_rp.oidc_django.views.authz_cb', name='authz_cb'),
    url(r'^logout$', 'django_rp.oidc_django.views.logout', name='logout'),

    url(r'^$', 'django_rp.views.home', name='home'),

    # Examples:
    # url(r'^access_web/', include('access_web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': path.join(BASEDIR, "static")})
)
