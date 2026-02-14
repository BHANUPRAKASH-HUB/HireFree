import requests
import json
import time

BASE_URL = "http://127.0.0.1:8001/api"

# Helper to print colored status
def print_status(message, status="INFO"):
    colors = {
        "INFO": "\033[94m",
        "SUCCESS": "\033[92m",
        "ERROR": "\033[91m",
        "RESET": "\033[0m"
    }
    print(f"{colors.get(status, '')}[{status}] {message}{colors['RESET']}")

def run_test():
    session = requests.Session()
    
    # ---------------------------------------------------------
    # 1. RECRUITER FLOW
    # ---------------------------------------------------------
    print_status("--- Starting Recruiter Flow ---", "INFO")
    
    # Register Recruiter
    recruiter_email = f"recruiter_{int(time.time())}@example.com"
    recruiter_pass = "password123"
    
    print_status(f"Registering Recruiter: {recruiter_email}")
    res = session.post(f"{BASE_URL}/auth/register/", json={
        "email": recruiter_email,
        "password": recruiter_pass,
        "user_type": "recruiter"
    })
    
    if res.status_code != 201:
        print_status(f"Recruiter Registration Failed: {res.text}", "ERROR")
        return
    print_status("Recruiter Registered", "SUCCESS")

    # Login Recruiter
    print_status("Logging in Recruiter")
    res = session.post(f"{BASE_URL}/auth/login/", json={
        "email": recruiter_email,
        "password": recruiter_pass
    })
    if res.status_code != 200:
        print_status("Recruiter Login Failed", "ERROR")
        return
    recruiter_token = res.json()['access']
    recruiter_headers = {'Authorization': f'Bearer {recruiter_token}'}
    print_status("Recruiter Logged In", "SUCCESS")

    # Post a Job
    print_status("Posting a Job")
    job_data = {
        "title": "Senior Python Developer",
        "description": "Looking for an expert.",
        "job_type": "full_time",
        "experience_level": "senior",
        "pay_per_hour": 80,
        "location": "Remote",
        "required_skills": ["Python", "Django"],
        "tech_stack": ["AWS", "Docker"]
    }
    res = session.post(f"{BASE_URL}/jobs/", json=job_data, headers=recruiter_headers)
    if res.status_code != 201:
        print_status(f"Job Posting Failed: {res.text}", "ERROR")
        return
    job_id = res.json()['id']
    print_status(f"Job Posted (ID: {job_id})", "SUCCESS")

    # ---------------------------------------------------------
    # 2. FREELANCER FLOW
    # ---------------------------------------------------------
    print_status("\n--- Starting Freelancer Flow ---", "INFO")

    # Register Freelancer
    freelancer_email = f"freelancer_{int(time.time())}@example.com"
    freelancer_pass = "password123"
    
    print_status(f"Registering Freelancer: {freelancer_email}")
    res = session.post(f"{BASE_URL}/auth/register/", json={
        "email": freelancer_email,
        "password": freelancer_pass,
        "user_type": "freelancer"
    })
    
    if res.status_code != 201:
        print_status(f"Freelancer Registration Failed: {res.text}", "ERROR")
        return
    print_status(f"Freelancer Registered. Status: {res.status_code}", "SUCCESS")

    # Login Freelancer
    print_status("Logging in Freelancer...", "INFO")
    try:
        res = session.post(f"{BASE_URL}/auth/login/", json={
            "email": freelancer_email,
            "password": freelancer_pass
        })
        print_status(f"Login Response: {res.status_code}", "INFO")
    except Exception as e:
        print_status(f"Login Exception: {e}", "ERROR")
        return

    if res.status_code != 200:
        print_status(f"Freelancer Login Failed: {res.text}", "ERROR")
        return
    freelancer_token = res.json()['access']
    freelancer_headers = {'Authorization': f'Bearer {freelancer_token}'}
    # Get Freelancer ID
    freelancer_id = session.get(f"{BASE_URL}/users/me/", headers=freelancer_headers).json()['id']
    print_status(f"Freelancer Logged In (ID: {freelancer_id})", "SUCCESS")

    # Update Profile
    print_status("Updating Freelancer Profile")
    profile_data = {
        "bio": "I code things.",
        "skills": ["Python", "JavaScript"],
        "tech_stack": ["Django", "React"],
        "hourly_rate": 50
    }
    res = session.put(f"{BASE_URL}/users/profile/", json=profile_data, headers=freelancer_headers)
    if res.status_code != 200:
        print_status(f"Profile Update Failed: {res.text}", "ERROR")
    else:
        print_status("Profile Updated", "SUCCESS")

    # Browse Jobs (Filter)
    print_status("Browsing Jobs (Filtering by Python)")
    res = session.get(f"{BASE_URL}/jobs/?search=Python", headers=freelancer_headers)
    if res.status_code == 200 and len(res.json()['results']) > 0:
        print_status(f"Jobs Found: {len(res.json()['results'])}", "SUCCESS")
    else:
        print_status("No Jobs Found", "ERROR")

    # Apply to Job
    print_status(f"Applying to Job ID: {job_id}")
    res = session.post(f"{BASE_URL}/jobs/{job_id}/apply/", json={"cover_letter": "Hire me!"}, headers=freelancer_headers)
    if res.status_code != 201:
        print_status(f"Application Failed: {res.text}", "ERROR")
        return
    application_id = res.json()['id']
    print_status(f"Applied Successfully (App ID: {application_id})", "SUCCESS")

    # ---------------------------------------------------------
    # 3. RECRUITER REVIEW
    # ---------------------------------------------------------
    print_status("\n--- Recruiter Review ---", "INFO")
    
    # Check Notifications
    print_status("Checking Recruiter Notifications")
    res = session.get(f"{BASE_URL}/notifications/unread/", headers=recruiter_headers)
    if res.status_code == 200:
        print_status(f"Unread Notifications: {len(res.json()['results'])}", "SUCCESS")
    else:
        print_status("Failed to fetch notifications", "ERROR")

    # View Applications
    print_status("Fetching Applications")
    res = session.get(f"{BASE_URL}/applications/", headers=recruiter_headers)
    apps = res.json()['results']
    target_app = next((a for a in apps if a['id'] == application_id), None)
    
    if target_app:
        print_status("Application Found", "SUCCESS")
        
        # Shortlist
        print_status("Shortlisting Application")
        res = session.patch(f"{BASE_URL}/jobs/applications/{application_id}/status/", json={"status": "interviewing"}, headers=recruiter_headers) # Note: API endpoint in dashboard.js was /status/ but verify views
        # Checking views.py: ApplicationStatusView is at 'jobs/applications/<int:pk>/status/' ?? or similar.
        # Let's assume standard REST. In views.py it was UpdateApplicationStatusView but URL?
        # Actually in dashboard.js it calls `/api/jobs/applications/${appId}/status/`
        # Let's try that.
        
        if res.status_code == 200:
             print_status("Application Shortlisted", "SUCCESS")
        else:
             print_status(f"Status Update Failed: {res.status_code} - {res.text}", "ERROR")

    else:
        print_status("Application Not Found in List", "ERROR")

    # ---------------------------------------------------------
    # 4. MESSAGING
    # ---------------------------------------------------------
    print_status("\n--- Messaging Flow ---", "INFO")
    
    # Recruiter sends message to Freelancer
    print_status("Recruiter sending message")
    msg_data = {
        "recipient": freelancer_id,
        "content": "Hello, let's schedule an interview."
    }
    res = session.post(f"{BASE_URL}/messages/", json=msg_data, headers=recruiter_headers)
    if res.status_code == 201:
        print_status("Message Sent", "SUCCESS")
    else:
        print_status(f"Message Sending Failed: {res.text}", "ERROR")

    # Freelancer checks messages
    print_status("Freelancer checking messages")
    res = session.get(f"{BASE_URL}/messages/", headers=freelancer_headers)
    messages = res.json()
    if len(messages) > 0:
        print_status(f"Freelancer received {len(messages)} message(s)", "SUCCESS")
        print(f"Message Content: {messages[-1]['content']}")
    else:
        print_status("Freelancer received NO messages", "ERROR")

    print_status("TEST COMPLETED", "INFO")

if __name__ == "__main__":
    try:
        run_test()
    except Exception as e:
        print_status(f"Test Execution Error: {e}", "ERROR")
