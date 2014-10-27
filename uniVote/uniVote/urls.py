from django.conf.urls import patterns, include, url
from django.contrib import admin

# When a user requests a page from us, These URL patterns are checked first:
urlpatterns = patterns(
    '',
    # Examples:
    # Test EX: root url www.mysite.com/
    #url(r'^$', include('accounts.urls')),
    url(r'^elections/', include('elections.urls', namespace='elections')),
    url(r'^admin/', include(admin.site.urls)),
    # ex: accounts/...
    url(r'^accounts/', include('accounts.urls')),
)
