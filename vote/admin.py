from django.contrib import admin
from .models import ElectionManager,Candidate,Election,ElectionCampaign,ElectionOfficer,PresidingOfficer,User,Vote,Voter

admin.site.register(ElectionManager)
admin.site.register(Candidate)
admin.site.register(Election)
admin.site.register(ElectionCampaign)
admin.site.register(ElectionOfficer)
admin.site.register(PresidingOfficer)
admin.site.register(Vote)
admin.site.register(Voter)

