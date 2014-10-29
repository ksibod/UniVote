from django.db import models
from django.utils import timezone as tz
from django.contrib.auth.models import User

# AFTER CHANGING MODELS, issue commands makemigrations, migrate to save in db.


# this Election class is represented in the db
class Election(models.Model):
    def __unicode__(self):
        return self.election_text

    def in_election_window(self):
        if tz.now() > self.start_date and tz.now() < self.end_date:
            return True
        else:
            return False

    election_text = models.CharField(max_length=200)
    start_date = models.DateTimeField('date election starts')
    end_date = models.DateTimeField('date election ends')

    in_election_window.admin_order_field = 'start_date'
    in_election_window.boolean = True
    in_election_window.short_description = 'In election window?'


# Each candiate is represented in the db
class Candidate(models.Model):
    def __unicode__(self):
        return self.candidate_name
    # each candidate is related to an election
    election = models.ForeignKey(Election)
    candidate_name = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


# Extending the existing User model to allow user to vote once per election:
# https://docs.djangoproject.com/en/1.7/topics/auth/customizing/#extending-the-existing-user-model
class Voter(models.Model):
    user = models.ForeignKey(User)
    # user = models.OneToOneField(User)
    election = models.ForeignKey(Election)
    approved = models.BooleanField(default=False)


    def is_approved(self):
        if self.approved:
            return True
        else:
            return False
