from django.db import models
from django.conf import settings
from users.models import Skill, TechStack

class Job(models.Model):
    EXPERIENCE_LEVELS = [
        ('junior', 'Junior'),
        ('mid', 'Mid-level'),
        ('senior', 'Senior'),
    ]
    JOB_TYPES = [
        ('full_time', 'Full-time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance Project'),
        ('part_time', 'Part-time'),
    ]
    
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    required_skills = models.ManyToManyField(Skill, blank=True)
    tech_stack = models.ManyToManyField(TechStack, blank=True)
    
    pay_per_hour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_range = models.CharField(max_length=100, blank=True, help_text="Text description e.g. '$50-100k/yr'") # Keeping for backward compat/flexibility
    
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVELS, default='mid')
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default='contract')
    location = models.CharField(max_length=100, default='Remote')
    
    deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interviewing', 'Interviewing'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    freelancer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)
    
    resume_snapshot = models.FileField(upload_to='application_resumes/', null=True, blank=True)

    class Meta:
        unique_together = ['job', 'freelancer']

    def __str__(self):
        return f"{self.freelancer.email} -> {self.job.title}"
