from django.contrib import admin
from elections.models import Candidate, Election


# Register your models here.
class CandidateInLine(admin.TabularInline):
    model = Candidate
    extra = 3


# This class represents the properties avaiable oat the admin panel at /admin/:
class ElectionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['election_text']}),
        ('Election Window',    {'fields': [('start_date', 'end_date')]}),
    ]
    inlines = [CandidateInLine]
    list_display = (
        'election_text',
        'start_date',
        'end_date',
        'in_election_window'
        )
    list_filter = ['start_date']
    search_fields = ['election_text']


admin.site.register(Election, ElectionAdmin)
