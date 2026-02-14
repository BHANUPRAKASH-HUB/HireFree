from django.contrib import admin
from .models import User, FreelancerProfile, RecruiterProfile, Skill, TechStack

admin.site.register(User)
admin.site.register(FreelancerProfile)
admin.site.register(RecruiterProfile)
admin.site.register(Skill)
admin.site.register(TechStack)
