from django.db import models
from django.utils import timezone as tz
from django.contrib.auth.models import User

## AFTER CHANGING MODELS, issue commands makemigrations, migrate to save in db.


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
    race_detail = models.CharField(max_length=200, default='')


# Each candiate is represented in the db.
# They are specifically bound to a race.
class Candidate(models.Model):
    def __unicode__(self):
        return self.candidate_name

    # each Candidate is related to an race in an election
    race = models.ForeignKey(Race)
    election = models.ForeignKey(Election)
    candidate_name = models.CharField(max_length=200)


# Extending the existing User model to allow user to vote once per election:
# https://docs.djangoproject.com
# /en/1.7/topics/auth/customizing/#extending-the-existing-user-model
class Voter(models.Model):
    user = models.ForeignKey(User)
    # user = models.OneToOneField(User)
    election = models.ForeignKey(Election)

    # Hold election information for each user
    # This is a dict that holds each election that the voter is approved for.
    # After voting, set that election to false, so they can no longer vote.
    elections = {models.ForeignKey(Election): True}
    #approved = models.BooleanField(default=False)

    def is_approved(self, election_name):
        #iterate through user 'elections' dictionary
        for i, test in self.elections:
            if i.election_text == election_name:
                #if approved and value is true
                if test:
                    return True
                #if approved but already voted
                else:
                    return False
        # Voter is not approved for this election
        return False

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


## Stores votes in a table with foreign keys to respective attributes
class Votes(models.Model):
    def __unicode__(self):
        return self.votes_id

    # Votes are stored by votes cast for cand by voter in race
    race_voted_in = models.ForeignKey(Race)
    voter_who_voted = models.ForeignKey(Voter)
    candidate_voted_for = models.ForeignKey(Candidate)
