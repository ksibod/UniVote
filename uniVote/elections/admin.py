from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from models import *

## This class places candidate creation in the admin-race creation panel
class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 1

## This class places voter assignements in the admin panel under elections
class VoterInline(admin.TabularInline):
    model = Voter
    verbose_name_plural = 'Voter Approval'
    
## This adds a race to a givem election under the admin panel    
class RaceInline(admin.TabularInline):
    model = Race
    extra = 1

## This class represents the properties avaiable at the admin panel at /admin/:
class ElectionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['election_text']}),
        ('Election Window',    {'fields': [('start_date', 'end_date')]}),
    ]
    inlines = [
                RaceInline, CandidateInline, VoterInline
                ]
    list_display = (
        'election_text',
        'start_date',
        'end_date',
        'in_election_window'
        )
    list_filter = ['start_date']
    search_fields = ['election_text']

## Registers the used classes for the admin panel
admin.site.unregister(User)
admin.site.register(Election, ElectionAdmin)
admin.site.register(User, UserAdmin)
