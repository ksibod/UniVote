from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    # ex: /accounts/login/
    # url(r'^login/$', 'accounts.views.user_login'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name':
        'accounts/login.html'}),
    # ex: /accounts/logout/
    url(r'^logout/$', 'accounts.views.user_logout'),
    # ex: /accounts/register/
    url(r'^register/$', 'accounts.views.user_register'),
    )
