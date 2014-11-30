from django.db import models
from django import forms
from django.utils import timezone as tz
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

## AFTER CHANGING MODELS, issue commands makemigrations, migrate to save in db.

STATUS_CHOICES = (
    ('a', 'Approved'),
    ('n', 'Not Approved')
)


## Election class is represented in the db, it is a container for races
class Election(models.Model):
    def __unicode__(self):
        return self.election_text

    def in_election_window(self):
        if tz.now() > self.start_date and tz.now() < self.end_date:
            return True
        else:
            return False

    def is_closed(self):
        if tz.now() > self.end_date:
            return True
        else:
            return False

    election_text = models.CharField(max_length=200)
    start_date = models.DateTimeField('date election starts')
    end_date = models.DateTimeField('date election ends')

    in_election_window.admin_order_field = 'start_date'
    in_election_window.boolean = True
    in_election_window.short_description = 'In election window?'


## Race class represented in the database, it is a container for Candidates
class Race(models.Model):
    def __unicode__(self):
        return self.race_name

    # each race is related to an election
    election = models.ForeignKey(Election)
    race_name = models.CharField(max_length=200, default='')
    race_description = models.CharField(max_length=200, default='')
    race_detail = models.CharField(max_length=1000, default='')


# Each candiate is represented in the db.
# They are specifically bound to a race.
class Candidate(models.Model):
    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name

    # each Candidate is related to an race in an election
    race = models.ForeignKey(Race)
    election = models.ForeignKey(Election)
    ## Using the line below forces the admin to place a candidate in a race before
    ## creating an election. It's a catch-22.
    #user = models.ForeignKey(User, default='') #checking if this is causing a bug
    user = models.ForeignKey(User)

## Hold data used in a candidate profile page.
class Profile(models.Model):
    def __unicode__(self):
        return self.id

    # Information stored in profile page
    #race = models.ForeignKey(Race)
    #election = models.ForeignKey(Election)
    candidate = models.ForeignKey(Candidate, default='')
    major = models.CharField(max_length=100, default='')
    interests = models.CharField(max_length=200, default='')
    experience = models.CharField(max_length=200, default='')


## Form to handle profile data
class ProfileForm(forms.Form):
    class Meta:
        model = Profile
        fields = ['major', 'interests', 'experience']


# Extending the existing User model to allow user to vote once per election:
# https://docs.djangoproject.com
# /en/1.7/topics/auth/customizing/#extending-the-existing-user-model
class Voter(models.Model):

    user = models.ForeignKey(User)
    election = models.ForeignKey(Election)
    is_approved = models.CharField(max_length=1, choices=STATUS_CHOICES, default='n')
    approved = models.BooleanField(default=False, editable=False)

    # bool value to check if the approval status has already been set to approved
    already_sent = models.BooleanField(default=False, editable=False)

    #bool to show if they have voted or not
    has_voted = models.BooleanField(default=False, editable=False)

    #store the confirmation num
    confirmation = models.CharField(max_length=40, default="")

    # send email when voters have been approved
    def send_approval_email(self):
        if self.already_sent:
            return
        else:
            user = str(self.user.username)
            election_name = str(self.election.election_text)
            email = EmailMessage("Voter Registration", "You have been approved to vote in the following election.\n\n"
                                                       "Username: " + user + "\n"
                                                       "Election: " + election_name + "\n\n"
                                                       "Thank you for using our system!"
                                                       "\nuniVote team", to=[self.user.email])
            email.send()
            return

    #check if they are approved
    def check_approval(self):
        if self.is_approved is "Approved":
            self.approved = True
            return True
        else:
            self.approved = False
            return False

    # Hold election information for each user
    # This is a dict that holds each election that the voter is approved for.
    # After voting, set that election to false, so they can no longer vote.
    #elections = {models.ForeignKey(Election): True}
    #approved = models.BooleanField(default=False)

    def add_election(self, election_object):
        self.elections.update({election_object: True})

    def delete_election(self, election_object):
        for i, test in self.elections:
            if i == election_object:
                del self.elections[i]
                break

    def update_vote_status(self, election_object):
        for i, test in self.elections:
            if i == election_object:
                # change from true to false
                if test:
                    self.elections[i] = False
                # change from false to true
                else:
                    self.elections[i] = True

    def as_dict(self):
        return {
            #'all_votes': self.all_votes,
            'id': self.id,
            'user': self.user,
            'election_id': self.election,
        }

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name


## Stores votes in a table with foreign keys to respective attributes
class Votes(models.Model):

    # Votes are stored by votes cast for cand by voter in race
    race_voted_in = models.ForeignKey(Race)
    voter_who_voted = models.ForeignKey(Voter)
    candidate_voted_for = models.ForeignKey(Candidate)
