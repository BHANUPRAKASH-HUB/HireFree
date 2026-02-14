from django.contrib import admin
from .models import Job, JobApplication

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'recruiter', 'job_type', 'experience_level', 'pay_per_hour', 'created_at')
    list_filter = ('job_type', 'experience_level')
    search_fields = ('title', 'description')

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('freelancer', 'job', 'status', 'applied_at')
    list_filter = ('status',)

admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
