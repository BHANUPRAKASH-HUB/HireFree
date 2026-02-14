import os
import django
import sys
from pathlib import Path
from datetime import date

# Setup Django Environment
sys.path.append(str(Path(__file__).resolve().parent / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from jobs.models import Job, JobApplication
from users.models import FreelancerProfile, RecruiterProfile, Skill, TechStack
from messaging.models import Message

User = get_user_model()

def populate():
    print("Creating Demo Data (V2)...")

    # Skills & Tech Stack
    python, _ = Skill.objects.get_or_create(name='Python')
    react, _ = Skill.objects.get_or_create(name='React')
    django_skill, _ = Skill.objects.get_or_create(name='Django')
    
    aws, _ = TechStack.objects.get_or_create(name='AWS')
    docker, _ = TechStack.objects.get_or_create(name='Docker')

    # Create Recruiter
    r1, _ = User.objects.get_or_create(email='recruiter@example.com', defaults={'user_type': 'recruiter'})
    r1.set_password('password123')
    r1.save()
    rp, _ = RecruiterProfile.objects.get_or_create(user=r1, defaults={'company_name': 'Tech Corp', 'bio': 'Hiring top talent.'})

    print("Recruiters created.")

    # Create Freelancer
    f1, _ = User.objects.get_or_create(email='freelancer@example.com', defaults={'user_type': 'freelancer'})
    f1.set_password('password123')
    f1.save()
    fp, _ = FreelancerProfile.objects.get_or_create(user=f1, defaults={
        'bio': 'Full Stack Dev', 
        'years_of_experience': 5,
        'hourly_rate': 60.00
    })
    fp.skills.add(python, django_skill)
    fp.tech_stack.add(docker)
    fp.save()

    print("Freelancers created.")

    # Create Job
    j1, _ = Job.objects.get_or_create(
        title='Senior Django Logic Expert',
        recruiter=r1,
        defaults={
            'description': 'Refactoring backend systems.',
            'pay_per_hour': 80.00,
            'experience_level': 'senior',
            'job_type': 'contract'
        }
    )
    j1.required_skills.add(django_skill, python)
    j1.tech_stack.add(aws)
    j1.save()
    
    print("Jobs created.")

    # Create Application
    if not JobApplication.objects.filter(job=j1, freelancer=f1).exists():
        JobApplication.objects.create(
            job=j1,
            freelancer=f1,
            cover_letter="I am the best for this.",
            status='interviewing'
        )

    # Create Message
    Message.objects.create(
        sender=r1,
        recipient=f1,
        content="Hi, checked your profile. When can we talk?"
    )

    print("Applications & Messages created.")
    print("Done! Login: recruiter@example.com / password123")

if __name__ == '__main__':
    populate()
