from django.conf.urls import patterns, url

# These urlpatterns are responsible for handling urls starting with:
# /accounts/...    :
urlpatterns = patterns(
    '',
    # ex: /
    url(r'^$', 'django.contrib.auth.views.login', {'template_name':
        'accounts/login.html'}, "login_page"),
    #url(r'^login/$', 'django.contrib.auth.views.login', {'template_name':
    #    'accounts/login.html'}),
    # ex: /accounts/logout/
    url(r'^logout/$', 'accounts.views.user_logout'),
    # ex: /accounts/register/
    url(r'^register/$', 'accounts.views.user_register'),
    )
