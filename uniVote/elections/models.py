from django.db import models
from django.utils import timezone as tz


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


class Candidate(models.Model):
    def __unicode__(self):
        return self.candidate_name
    election = models.ForeignKey(Election)
    candidate_name = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
