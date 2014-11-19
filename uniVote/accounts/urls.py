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
    )
