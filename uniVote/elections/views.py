from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from elections.models import Race, Candidate, Election, Voter

class IndexView(generic.ListView):
    template_name = 'elections/index.html'
    context_object_name = 'latest_election_list'

    def get_queryset(self):
        """Return the last five published elections."""
        return Election.objects.order_by('-start_date')[:5]


class DetailView(generic.DetailView):
    model = Election
    template_name = 'elections/detail.html'


class ResultsView(generic.DetailView):
    model = Election
    template_name = 'elections/results.html'


# Called whenever a user makes a vote:
### HERE SHOULD CHECK IF request.user is authenticated BEFORE THEY CAN VOTE:
def vote(request, race_id):
    p = get_object_or_404(Race, pk=race_id)
    try:
        selected_candidate = p.candidate_set.get(pk=request.POST['candidate'])
    except (KeyError, Candidate.DoesNotExist):
        # Redisplay the election voting form:
        return render(request, 'elections/detail.html', {
            'election': p,
            'error_message': 'You didn\'t select a candidate.',
        })
    else:
        selected_candidate.votes += 1
        selected_candidate.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('elections:results', args=(p.id,)))
