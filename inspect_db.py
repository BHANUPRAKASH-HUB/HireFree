import os
import django
import sys
from pathlib import Path

# Setup Django Environment
# Add 'backend' to sys.path so we can import 'config'
sys.path.append(str(Path(__file__).resolve().parent / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from jobs.models import Job, JobApplication
from users.models import FreelancerProfile, RecruiterProfile
from messaging.models import Message

User = get_user_model()

def inspect():
    print("-" * 50)
    print("DATABASE INSPECTION")
    print("-" * 50)

    print(f"\n[USERS] Total: {User.objects.count()}")
    for u in User.objects.all():
        print(f" - {u.email} ({u.user_type})")

    print(f"\n[PROFILES]")
    print(f" - Freelancers: {FreelancerProfile.objects.count()}")
    print(f" - Recruiters: {RecruiterProfile.objects.count()}")

    print(f"\n[JOBS] Total: {Job.objects.count()}")
    for j in Job.objects.all():
        print(f" - {j.title} (${j.pay_per_hour}/hr) [{j.job_type}]")

    print(f"\n[APPLICATIONS] Total: {JobApplication.objects.count()}")
    for a in JobApplication.objects.all():
        print(f" - {a.freelancer.email} -> {a.job.title} ({a.status})")

    print(f"\n[MESSAGES] Total: {Message.objects.count()}")
    for m in Message.objects.all():
        print(f" - From {m.sender.email} to {m.recipient.email}: '{m.content[:30]}...'")

    print("-" * 50)

if __name__ == '__main__':
    inspect()
