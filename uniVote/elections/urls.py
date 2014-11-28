from django.conf.urls import patterns, url

import views
import models

urlpatterns = patterns(
    '',

    # EX: /elections/
    url(r'^$',
        views.IndexView.as_view(),
        name='index'),

    # EX: /elections/alertUsers/
    url(r'^alertUsers/$',
        views.AlertUsers.as_view(),
        name='alertUsers'),

    # EX: /elections/sendingAlerts
    url(r'^sendingAlerts/$',
        views.sendAlerts,
        name='sendAlerts'),

    # EX: /elections/alertsSent
    url(r'^alertsSent/$',
        views.AlertsSent.as_view(),
        name='alertsSent'),

    # EX: /elections/monitor/
    url(r'^monitor/$',
        views.MonitorView.as_view(),
        name='monitor'),

    # EX: /elections/4
    url(r'^(?P<pk>\d+)/$',
        views.DetailView.as_view(),
        name='detail'),

    # EX: /elections/4/results
    url(r'^(?P<pk>\d+)/results/$',
        views.ResultsView.as_view(),
        name='results'),

    # EX: /elections/4/vote
    url(r'^(?P<election_id>\d+)/vote/$',
        views.vote,
        name='vote'),

    url(r'^election_register/(?P<election_id>\d+)/$',
        views.election_register,
        name='election_register'),

    # ex: /elections/4/voteform
    url(r'^(?P<pk>\d+)/voteform/$',
        views.VoteFormView.as_view(),
        name='voteform'),

    url(r'^profile/(?P<pk>\d+)/$',
        views.profile,
        name='profile'),

    url(r'^candidate_register/(?P<race_id>\d+)/$',
        views.candidate_register,
        name='candidate_register'),

    url(r'^(?P<pk>\d+)$',
        views.HybridDetailView.as_view(model=models.Voter)),
    )
