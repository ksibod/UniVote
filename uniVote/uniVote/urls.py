from django.conf.urls import patterns, include, url
from django.contrib import admin

# When a user requests a page from us, These URL patterns are checked first:
urlpatterns = patterns(
    '',
    # Examples:
    # EX: /
    url(r'', include('accounts.urls')),
    # EX: /elections/
    url(r'^elections/', include('elections.urls', namespace='elections')),
    # EX: /admin/
    url(r'^admin/', include(admin.site.urls)),
    # EX: /accounts/...
    url(r'^accounts/', include('accounts.urls')),
)
