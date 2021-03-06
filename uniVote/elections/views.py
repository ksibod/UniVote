from django.shortcuts import get_object_or_404, render, redirect, render_to_response
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

        for voter in Voter.objects.all():
            if voter.election_id in voter_in_election.keys():
                # add election and its first voter
                voter_in_election[voter.election_id].append(voter.user.id)
            else:
                # create new array in this slot:
                voter_in_election[voter.election_id] = [voter.user.id]
                
        # Get dict of races and their candidates:
        # {'race': ['cand1', 'cand2', 'cand3']}
        race_and_candidates = {}
        for candidate in Candidate.objects.all():
            if candidate.race in race_and_candidates.keys():
                # add race and its first candidate
                race_and_candidates[candidate.race].append(
                    candidate.user.id)
            else:
                # create new array in this slot:
                race_and_candidates[candidate.race] = [
                    candidate.user.id]
                    
        context['races'] = race_and_candidates
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
    user_elections = []
    needs_to_vote = False

    # Make string of election names of active elections:
    for election in Election.objects.all():
        if election.in_election_window():
            active_elections.append(election)

    #print active_elections
    # for candidate in Candidate.objects.all():
    #     users_to_email.append(candidate.user)

    # go through the voter objects and find the ones that have not yet voted in the open elections
    not_voted = Voter.objects.filter(has_voted=False)
    #print not_voted
    for voter in not_voted:
        #print voter
        for electionid in active_elections:
            #print str(voter.election_id)
            #print str(electionid.id)
            if str(voter.election_id) == str(electionid.id):
                if voter.approved:
                    #print "THE SAME!"
                    needs_to_vote = True
                    user_elections.append(electionid)
                    continue

        if needs_to_vote:
            #print user_elections
            message = 'Hello %s %s! \n\nThis is just a reminder to vote in the election(s) that you are ' \
                      'registered for before the election window is over.' \
                      '\n' % (voter.user.first_name, voter.user.last_name)

            message += "The elections and their corresponding end dates/times are listed below:\n"
            for election in user_elections:
                message += "\t" + election.election_text + '\t' + str(election.end_date) + "\n"

            message += "\nThanks,\nuniVote team"
            email_address = voter.user.email
            email = EmailMessage('Voting Reminder', message, to=[email_address])
            email.send()
            needs_to_vote = False
            user_elections = []

    return redirect('/elections/alertsSent')


class AlertsSent(generic.TemplateView):
    template_name = 'elections/alertsSent.html'


# Handles candidate profile requests. PK refers to the Candidate
# user_id. Be aware there is a profile id and a candidate id. They are not equal.
def profile(request, pk):
    print pk + "yoloyoloyolo"
    candidates = Candidate.objects.filter(user_id=pk)

    # Handles candidates in multiple elections.
    for c in candidates:
        candidate = c
        
    #If request is POST, process the form data
    if request.method == 'POST':
        # Make a form and populate with data.
        form = ProfileForm(request.POST)

        # Check if form is valid
        if form.is_valid():

            # All the fields in the profile are filled in here.
            my_profile = Profile(
                            candidate_id = candidate.id,
                            major = request.POST.get('major'),
                            experience = request.POST.get('experience'),
                            interests = request.POST.get('interests'),
            )
            my_profile.save()

            # Request is sent back to corresponding page.
            return render(request, 'elections/profile.html',
                {
                    'form': form,
                    'profile': my_profile,
                    'candidate': candidate,
                })
    else:
        # If request is a GET, then create a blank form and send back fields.
        form = ProfileForm()

        try:
            # Create a profile object to check if exists.
            my_profile = Profile.objects.get(candidate_id=candidate.id)

        except (KeyError, Profile.DoesNotExist):
            # If there is no candidate, then throw error and display data.
            return render(request, 'elections/profile.html',
                {
                    'candidate': candidate,
                    'error_message': 'This candidate does not have a profile.',
                })
        else:
            # Profile exists return profile, form and candidate data.
            return render(request, 'elections/profile.html',
                {
                    'form': form,
                    'profile': my_profile,
                    'candidate': candidate,
                })


#https://cloud.google.com/appengine/articles/django-nonrel#rh
class ResultsView(generic.DetailView):
    model = Election
    template_name = 'elections/results.html'


def get_vote_data(request):

    return


    # def get_context_data(self, **kwargs):
    #     context = super(ResultsView, self).get_context_data(**kwargs)
    #
    #     # Get dict of candidate and their votes:
    #     # {'candidate1': XX, 'candidate2': XX}
    #     vote_totals = {}
    #
    #     for vote in Votes.objects.all():
    #         if vote.candidate_voted_for not in vote_totals.keys():
    #             # add candidate and their first vote to the dict:
    #             vote_totals[vote.candidate_voted_for] = 1
    #         else:
    #             # increment candidates vote count by 1:
    #             vote_totals[vote.candidate_voted_for] += 1
    #
    #     # Get dict of races and their candidates:
    #     # {'race': ['cand1', 'cand2', 'cand3']}
    #     race_and_candidates = {}
    #     for candidate in Candidate.objects.all():
    #         if candidate.race in race_and_candidates.keys():
    #             # add race and its first candidate
    #             race_and_candidates[candidate.race].append(
    #                 candidate.user.last_name)
    #         else:
    #             # create new array in this slot:
    #             race_and_candidates[candidate.race] = [
    #                 candidate.user.last_name]
    #
    #     context['votes'] = vote_totals
    #     context['races'] = race_and_candidates
    #     return context
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
    total = int(election_id)+int(request.user.id)+100

    # check if the user has already registered for this election
    already_registered = Voter.objects.filter(user_id=request.user.id)
    #print already_registered
    for voter in already_registered:
        if str(voter.election_id) == str(election_id):
            #user is already registered
            return HttpResponse("alreadyRegistered")

    ## Creates a new Candidate object and save in the database
    new_voter = Voter(
                        # Kludging id because DB is being screwy.
                        id=str(total),
                        user_id=request.user.id,
                        election_id=election_id,
                        # changed these so that they are not approved by default  KS
                        approved=0,
                        is_approved='n',
    )
    new_voter.save()

    #get the election name to email to user
    election = Election.objects.get(pk=election_id)
    #print election
    #notify user that they have registered to vote
    user = str(request.user.username)
    #print user
    email = EmailMessage("Voter Registration", "Username: " + user + "\n"
                                               "Election: " + str(election) + "\n\n"
                                               "Thanks for registering to vote with uniVote!"
                                               " \nWe will send you another email when you have been approved."
                                               "\n\nThanks,\nuniVote team", to=[request.user.email])
    email.send()

    ## Returns the user to the previous screen as a registered user.
    #return redirect('/elections/'+ election_id + '/')
    return HttpResponse("registeredVoter")

                                    
## Function called when a user clicks a button to register as a candidate for a race.
def candidate_register(request, race_id):
    # Gets election objects
    race_object = get_object_or_404(Race, id=race_id)
    election_object = race_object.election
    election_id = election_object.id
    
    ## Creates a new Candidate object in the database
    new_candidate = Candidate(
                        race_id=race_id,
                        user_id=request.user.id,
                        election_id=election_id
                        )
    new_candidate.save()

    ## Returns the user to the previous screen as a registered candidate.
    return redirect('/elections/' + str(election_id) + '/')
    
   
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
    total_votes = []
    votes_for_candidates = []

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
            #print voter
            #print voter.user_id
            #print request.user.id
            if voter.user_id == request.user.id:
                user_approved = True
                new_key = voter.id

        if user_approved:
            user_object = get_object_or_404(Voter, pk=new_key)
        else:
            vote_success = False
            return HttpResponse("notApproved")

        # Cycle through the dynamic list of races and processes the Post data
        for race in races:
            try:
                # Instance objects need to be made to pass into the database
                race_object = get_object_or_404(Race, pk=race.id)
                candidate_object = get_object_or_404(
                    Candidate, pk=request.POST['candidate_race_' + str(race.id)])

            except (KeyError, Candidate.DoesNotExist):
                vote_success = False
                return HttpResponse("noSelection")
            else:
                # Check for previous vote should go here,
                # replacing vote if already voted, if not newvote
                vote_check = Votes.objects.filter(
                    race_voted_in=race_object,
                    voter_who_voted=user_object)

                if vote_check:
                    vote_success = False
                    return HttpResponse("alreadyVoted")

                else:
                    # Create a new database entry with the objects created above.
                    # Save the entry.
                    new_vote = Votes(race_voted_in=race_object,
                                     voter_who_voted=user_object,
                                     candidate_voted_for=candidate_object)
                    total_votes.append(new_vote)
                    votes_for_candidates.append(candidate_object)
                    people_voted_for.append("\t" + candidate_object.user.first_name + " " + candidate_object.user.last_name
                                            + "---- " + race_object.race_name + "\n")
                    vote_success = True

        if vote_success:
            # save the votes
            for votes in total_votes:
                votes.save()
            for candidates in votes_for_candidates:
                candidates.num_of_votes += 1
                candidates.save()

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
                      "You voted for: \n" + str(voted_for) + "\n" \
                      "Confirmation Number: " + confirmation_num

            email_address = request.user.email
            email = EmailMessage("Vote Confirmation", message, to=[email_address])
            email.send()

            #update the voter object
            user_object.has_voted = True
            user_object.confirmation = confirmation_num
            user_object.save()

            return HttpResponse("Done")
