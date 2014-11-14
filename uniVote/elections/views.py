from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views import generic

from models import *


class IndexView(generic.ListView):
    template_name = 'elections/index.html'
    context_object_name = 'latest_election_list'

    def get_queryset(self):
        """Return the last five published elections."""
        return Election.objects.order_by('-start_date')[:5]


class DetailView(generic.DetailView):
    model = Election
    template_name = 'elections/detail.html'


class VoteFormView(generic.DetailView):
    model = Election
    template_name = 'elections/voteform.html'


class MonitorView(generic.ListView):
    model = Election
    template_name = 'elections/monitor.html'

    def get_context_data(self, **kwargs):
        context = super(MonitorView, self).get_context_data(**kwargs)

        # Get dict of candidate and their votes:
        # {'candidate1': XX, 'candidate2': XX}
        vote_totals = {}
        for vote in Votes.objects.all():
            if vote.candidate_voted_for not in vote_totals.keys():
                # add candidate and their first vote to the dict:
                vote_totals[vote.candidate_voted_for] = 1
            else:
                # increment candidates vote count by 1:
                vote_totals[vote.candidate_voted_for] += 1

        # Get dict of races and their candidates:
        # {'race': ['cand1', 'cand2', 'cand3']}
        race_and_candidates = {}
        for candidate in Candidate.objects.all():
            if candidate.race in race_and_candidates.keys():
                # add race and its first candidate
                race_and_candidates[candidate.race].append(
                    candidate.candidate_name)
            else:
                # create new array in this slot:
                race_and_candidates[candidate.race] = [
                    candidate.candidate_name]

        context['votes'] = vote_totals
        context['races'] = race_and_candidates
        return context


# stackoverflow.com/questions/9046533/creating-user-profile-pages-in-django
class ProfileView(generic.DetailView):
    model = Profile
    template_name = 'elections/profile.html'

    def profile_exists(self):
        pass

    def get_object(self):
        """Return's the current users profile."""
        try:
            return self.request.user.get_profile()
        except Profile.DoesNotExist:
            raise NotImplemented(
                "What if the user doesn't have an associated profile?")


def vote(request, election_id):
    """
    Vote function called from an open election html. When a user casts a vote
    the function performs checks to ensure vote is unique by cross referencing
    the database. The form from the referring web page passes POST into this
    function. The data is extracted and processed.Assistance from David Adamo
    Jr. in writing this vote function and using the form POST queries.
    """

    # Gets election object
    election = get_object_or_404(Election, pk=election_id)
    # Gets a list of races that match the election id
    races = Race.objects.filter(election_id=election_id)

    # Cycle through the dynamic list of races and processes the Post data
    for race in races:
        try:
            # Instance objects need to be made to pass into the database
            race_object = get_object_or_404(Race, pk=race.id)
            user_object = get_object_or_404(Voter, pk=request.user.id)
            candidate_object = get_object_or_404(
                Candidate, pk=request.POST['candidate_race_' + str(race.id)])

        except (KeyError, Candidate.DoesNotExist):
            # Redisplay the election voting form:
            return render(
                request,
                'elections/voteform.html',
                {
                    'election': election,
                    'error_message': 'You didn\'t select a candidate.',
                })
        else:
            # Check for previous vote should go here,
            # replacing vote if already voted, if not newvote
            vote_check = Votes.objects.filter(
                race_voted_in=race_object,
                voter_who_voted=user_object)

            if vote_check:
                return render(
                    request,
                    'elections/voteform.html',
                    {
                        'election': election,
                        'error_message': 'You already voted in this race.',
                    })
            else:
                # Create a new databse entry with the objects created above.
                # Save the entry.
                new_vote = Votes(race_voted_in=race_object,
                                 voter_who_voted=user_object,
                                 candidate_voted_for=candidate_object)
                new_vote.save()

                # Send user to a page reporting success of vote
                """
                Always return an HttpResponseRedirect after successfully
                dealing with POST data. This prevents data from being posted
                twice if a user hits the Back button.
                """
                return HttpResponse("Done")
