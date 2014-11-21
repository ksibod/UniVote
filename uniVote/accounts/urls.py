from django.conf.urls import patterns, url

# These urlpatterns are responsible for handling urls starting with:
# /accounts/...    :
urlpatterns = patterns(
    '',
    # This is for the login page - we are overriding the django default login system and using our own
    # function "user_login" in accounts/views.py
    url(r'^$', 'accounts.views.user_login'),

    # For the logout function
    url(r'^logout/$', 'accounts.views.user_logout'),

    # For the register function
    url(r'^register/$', 'accounts.views.user_register'),

    # For sending email - forgot password
    url(r'^forgotPass/$', 'accounts.views.user_forgot_password'),

    # password reset templates
    url(r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset',
        {'post_reset_redirect' : '/accounts/password/reset/done/'}),
    url(r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect' : '/accounts/password/done/'}),
    url(r'^accounts/password/done/$', 'django.contrib.auth.views.password_reset_complete')
)
