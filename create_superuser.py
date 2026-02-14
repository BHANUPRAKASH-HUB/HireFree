import os
import django
import sys
from pathlib import Path

# Setup Django Environment
sys.path.append(str(Path(__file__).resolve().parent / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_admin():
    User = get_user_model()
    email = 'admin@example.com'
    password = 'adminpassword'
    
    if not User.objects.filter(email=email).exists():
        print(f"Creating superuser: {email}")
        User.objects.create_superuser(email=email, password=password)
        print("Superuser created successfully.")
    else:
        print(f"Superuser {email} already exists.")

if __name__ == '__main__':
    create_admin()
