from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', '/accounts/login'),
    url(r'^elections/', include('elections.urls', namespace='elections')),
    url(r'^admin/', include(admin.site.urls)),
    # ex: accounts/...
    url(r'^accounts/', include('accounts.urls')),
)
