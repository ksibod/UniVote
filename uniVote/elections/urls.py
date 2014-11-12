from django.conf.urls import patterns, url

from elections import views

urlpatterns = patterns(
    '',
    # ex: /elections/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /elections/4
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /elections/4/results
    url(r'^(?P<pk>\d+)/results/$',
        views.ResultsView.as_view(), name='results'),
    # ex: /elections/4/vote
    url(r'^(?P<election_id>\d+)/vote/$', views.vote, name='vote'),
    # ex: /elections/4/voteform
    url(r'^(?P<election_id>\d+)/voteform/$', views.vote, name='vote'),
    )
