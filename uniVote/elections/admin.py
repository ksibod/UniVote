from django.contrib import admin
from elections.models import Race, Candidate, Election, Voter
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 1

class VoterInline(admin.TabularInline):
    model = Voter
    verbose_name_plural = 'Voter Approval'

# This class represents the properties avaiable oat the admin panel at /admin/:
class ElectionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['election_text']}),
        ('Election Window',    {'fields': [('start_date', 'end_date')]}),
    ]
    inlines = [
                VoterInline
                ]
    list_display = (
        'election_text',
        'start_date',
        'end_date',
        'in_election_window'
        )
    list_filter = ['start_date']
    search_fields = ['election_text']
    
# This class represents the properties avaiable oat the admin panel at /admin/:
class RaceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['election']}),
        ('Position Title',     {'fields': ['race_name']}),
        ('Description',        {'fields': ['race_description']}),
        ('Full Detail',        {'fields': ['race_detail']}),
             ]
    inlines = [
                CandidateInline
            ]
    list_display = (
        'race_name',
        'race_description',
        'election',
        )

admin.site.unregister(User)
admin.site.register(Election, ElectionAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Race, RaceAdmin)
