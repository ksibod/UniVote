from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.views import generic
import json
from django.views.generic.detail import BaseDetailView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from models import *

# for emailing users with receipt
from django.core.mail import EmailMessage
import time
import uuid


class IndexView(generic.ListView):
    template_name = 'elections/index.html'
    context_object_name = 'latest_election_list'

    def get_queryset(self):
        """Return the last five published elections."""
        return Election.objects.order_by('-start_date')[:5]


class DetailView(generic.DetailView):
    model = Election
    template_name = 'elections/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        # Get dict of elections with all the voters:
        # {'election1': [ V1, V2, V3 ], 'election2': [v1, v2, v3 ],}
        voter_in_election = {}
        ##for voter in Voter.objects.all():
          ##  voter_total.update({ 'voter.id': [voter.user, voter.election] })
        for voter in Voter.objects.all():
            if voter.election_id in voter_in_election.keys():
                # add election and its first voter
                voter_in_election[voter.election_id].append(voter.id)
            else:
                # create new array in this slot:
                voter_in_election[voter.election_id] = [voter.id]

        context['voters'] = voter_in_election
        return context


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
                    candidate.user.first_name + ' ' + candidate.user.last_name)
            else:
                # create new array in this slot:
                race_and_candidates[candidate.race] = [
                    candidate.user.first_name + ' ' + candidate.user.last_name]

        context['votes'] = vote_totals
        context['races'] = race_and_candidates
        return context


class AlertUsers(generic.ListView):
    model = Election
    template_name = 'elections/alertUsers.html'
    context_object_name = 'active_elections'

    def get_queryset(self):
        active_elections = []
        for election in Election.objects.all():
            if election.in_election_window():
                active_elections.append(election.election_text)
        return active_elections


def sendAlerts(request):

    active_elections = []
    users_to_email = []

    # Make string of election names of active elections:
    for election in Election.objects.all():
        if election.in_election_window():
            # active_elections += (election.election_text + ' ')
            active_elections.append(election.election_text)

    for candidate in Candidate.objects.all():
        users_to_email.append(candidate.user)

    for user in users_to_email:
        message = 'Hello %s %s. This is a reminder to vote in the ' % (user.first_name, user.last_name)
        for election in active_elections:
            message += election + ' '

        message += ' election(s).'
        email_address = (user.email,)
        email = EmailMessage('Voting Reminder', message, to=email_address)
        email.send()

    return redirect('/elections/alertsSent')


class AlertsSent(generic.TemplateView):
    template_name = 'elections/alertsSent.html'

# stackoverflow.com/questions/9046533/creating-user-profile-pages-in-django
#class ProfileView(generic.DetailView):
 #   model = Election
  #  template_name = 'elections/profile.html'


def profile(request, pk):
    candidate = Candidate.objects.get(id=pk)

    try:
        # Gets candidate object
        my_profile = Profile.objects.get(candidate_id=pk)

    except (KeyError, Profile.DoesNotExist):
        # Redisplay the election voting form:
        return render(
            request,
            'elections/profile.html',
            {
                'candidate': candidate,
                'error_message': 'This candidate does not have a profile.',
            })
    else:
        return HttpResponseRedirect(
            reverse('elections:profile', args=(my_profile.candidate_id)))


#https://cloud.google.com/appengine/articles/django-nonrel#rh
class ResultsView(generic.DetailView):
    model = Election
    template_name = 'elections/results.html'

    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)

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
                    candidate.user.last_name)
            else:
                # create new array in this slot:
                race_and_candidates[candidate.race] = [
                    candidate.user.last_name]

        context['votes'] = vote_totals
        context['races'] = race_and_candidates
        return context
         #vote_counts.append(Votes.objects.filter(race_voted_in = race,
          #    candidate_voted_for = candidate_object))
         #total_election_votes += Votes.objects.filter.(race_id = race)


class JSONResponseMixin(object):
    def render_to_context(self, context):
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        return HttpResponse(
            content,
            content_type='application/json',
            **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        return json.dumps(context)


class HybridDetailView(JSONResponseMixin,
                       SingleObjectTemplateResponseMixin,
                       BaseDetailView):
    def render_to_response(self, context):
        if self.request_is_ajax():
            obj = context['object'].as_dict()
            return JSONResponseMixin.render_to_response(self, obj)
        else:
            return SingleObjectTemplateResponseMixin.render_to_response(
                self, context)


def election_register(request, election_id):
    # Gets election object
    election_object = get_object_or_404(Election, pk=election_id)
    user_object = get_object_or_404(Voter, pk=request.user.id)
    user_check = Voter.objects.filter(election_id=election_object,
                                      user_id=user_object)

    if request.method == 'GET':
        # If the user is registered in the election, then fail,
        # else do something.
        if user_check:
            # Redisplay the election voting form:
            return render(
                request,
                'elections/detail.html',
                {
                    'voter_id': user_check,
                    'election_object': election_object,
                    'message': 'You are already a candidate in this race.',
                })
        else:

            return render(
                request,
                'elections/detail.html',
                {
                    'voter_id': user_check,
                    'election_object': election_object,
                    'message': 'You are registered.',
                })

    elif request.method == 'POST':
        return HttpResponseRedirect(reverse('elections:election_register',
                                    args=(election.id,)))


def vote(request, election_id):
    """
    Vote function called from an open election html. When a user casts a vote
    the function performs checks to ensure vote is unique by cross referencing
    the database. The form from the referring web page passes POST into this
    function. The data is extracted and processed.Assistance from David Adamo
    Jr. in writing this vote function and using the form POST queries.
    """
    vote_success = False
    people_voted_for = []

    # Gets election object
    #election = get_object_or_404(Election, pk=election_id)
    # Gets a list of races that match the election id
    races = Race.objects.filter(election_id=election_id)

    # check if user is anonymous before casting the vote
    if request.user.is_anonymous():
        return HttpResponse("anonymous")

    else:

        user_approved = False
        new_key = 0
        approved_voters = Voter.objects.filter(approved=True)
        for voter in approved_voters:
            print voter
            print voter.user_id
            print request.user.id
            if voter.user_id == request.user.id:
                user_approved = True
                new_key = voter.id

        if user_approved:
            user_object = get_object_or_404(Voter, pk=new_key)
        else:
            return HttpResponse("notApproved")

        # Cycle through the dynamic list of races and processes the Post data
        for race in races:
            try:
                # Instance objects need to be made to pass into the database
                race_object = get_object_or_404(Race, pk=race.id)
                candidate_object = get_object_or_404(
                    Candidate, pk=request.POST['candidate_race_' + str(race.id)])

            except (KeyError, Candidate.DoesNotExist):
                return HttpResponse("noSelection")
            else:
                # Check for previous vote should go here,
                # replacing vote if already voted, if not newvote
                vote_check = Votes.objects.filter(
                    race_voted_in=race_object,
                    voter_who_voted=user_object)

                if vote_check:
                    return HttpResponse("alreadyVoted")

                else:
                    # Create a new databse entry with the objects created above.
                    # Save the entry.
                    new_vote = Votes(race_voted_in=race_object,
                                     voter_who_voted=user_object,
                                     candidate_voted_for=candidate_object)
                    new_vote.save()
                    people_voted_for.append(candidate_object.user.first_name + " " + candidate_object.user.last_name
                                            + "---- " + race_object + "\n")
                    vote_success = True

        if vote_success:
            # this is for emailing the confirmation receipt to the voter
            time_of_day = time.strftime("%I:%M")
            date = time.strftime("%m:%d:%Y")
            voted_for = ""
            for votes in people_voted_for:
                voted_for += votes

            x = uuid.uuid4()
            confirmation_num = str(x)

            message = "Thank you for voting with uniVote! \n\nBelow is a receipt with your vote details:\n\n\n" \
                      "Date: " + date + "\n" + "Time: " + time_of_day + "\n" \
                      "You voted for: " + str(voted_for) + "\n" \
                      "Confirmation Number: " + confirmation_num

            email_address = request.user.email
            email = EmailMessage("Vote Confirmation", message, to=[email_address])
            email.send()
            return HttpResponse("Done")
