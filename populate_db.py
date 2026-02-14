import os
import django
import sys
from pathlib import Path

# Setup Django Environment
sys.path.append(str(Path(__file__).resolve().parent / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from jobs.models import Job, Application
from users.models import Profile

User = get_user_model()

def populate():
    print("Creating Demo Data...")

    # Create Recruiters
    r1, _ = User.objects.get_or_create(email='recruiter1@example.com', defaults={'is_recruiter': True})
    r1.set_password('password123')
    r1.save()
    Profile.objects.get_or_create(user=r1, defaults={'bio': 'Tech Recruiter at Google'})

    r2, _ = User.objects.get_or_create(email='recruiter2@example.com', defaults={'is_recruiter': True})
    r2.set_password('password123')
    r2.save()
    Profile.objects.get_or_create(user=r2, defaults={'bio': 'Hiring Manager at Startup'})

    print("Recruiters created.")

    # Create Freelancers
    f1, _ = User.objects.get_or_create(email='freelancer1@example.com', defaults={'is_freelancer': True})
    f1.set_password('password123')
    f1.save()
    Profile.objects.get_or_create(user=f1, defaults={'bio': 'Full Stack Developer', 'skills': ['Python', 'React']})

    f2, _ = User.objects.get_or_create(email='freelancer2@example.com', defaults={'is_freelancer': True})
    f2.set_password('password123')
    f2.save()
    Profile.objects.get_or_create(user=f2, defaults={'bio': 'UI/UX Designer', 'skills': ['Figma', 'CSS']})

    print("Freelancers created.")

    # Create Jobs
    j1, _ = Job.objects.get_or_create(
        title='Senior Django Developer',
        recruiter=r1,
        defaults={
            'description': 'Looking for an expert in Django & DRF.',
            'requirements': '5+ years experience.',
            'salary_range': '$60-80/hr',
            'location': 'Remote'
        }
    )

    j2, _ = Job.objects.get_or_create(
        title='Frontend React Engineer',
        recruiter=r2,
        defaults={
            'description': 'Build beautiful UIs with React and Tailwind.',
            'requirements': 'Experience with modern JS.',
            'salary_range': '$40-60/hr',
            'location': 'New York, NY'
        }
    )
    
    print("Jobs created.")

    # Create Applications
    if not Application.objects.filter(job=j1, freelancer=f1).exists():
        Application.objects.create(
            job=j1,
            freelancer=f1,
            cover_letter="I am very interested in this role. Check my GitHub.",
            status='pending'
        )
    
    if not Application.objects.filter(job=j2, freelancer=f2).exists():
        Application.objects.create(
            job=j2,
            freelancer=f2,
            cover_letter="I have a great portfolio.",
            status='accepted'
        )

    print("Applications created.")
    print("Done! You can login with 'recruiter1@example.com' / 'password123'")

if __name__ == '__main__':
    populate()
