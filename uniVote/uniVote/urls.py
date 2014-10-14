from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'uniVote.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^elections/', include('elections.urls', namespace='elections')),
    url(r'^admin/', include(admin.site.urls)),
)
