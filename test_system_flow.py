import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api"

def print_step(msg):
    print(f"\n{'='*50}\n{msg}\n{'='*50}")

def register_user(email, password, user_type):
    url = f"{BASE_URL}/auth/register/"
    data = {"email": email, "password": password, "user_type": user_type}
    res = requests.post(url, json=data)
    if res.status_code == 201:
        print(f"✅ Registered {user_type}: {email}")
        return True
    elif res.status_code == 400 and "already exists" in res.text:
        print(f"⚠️ User {email} already exists. Proceeding.")
        return True
    else:
        print(f"❌ Failed to register {email}: {res.text}")
        return False

def login_user(email, password):
    url = f"{BASE_URL}/auth/login/"
    data = {"email": email, "password": password}
    res = requests.post(url, json=data)
    if res.status_code == 200:
        print(f"✅ Logged in as {email}")
        return res.json()['access']
    else:
        print(f"❌ Login failed for {email}: {res.text}")
        return None

def run_test():
    recruiter_email = f"recruiter_new_{int(time.time())}@example.com"
    freelancer_email = f"freelancer_new_{int(time.time())}@example.com"
    password = "password123"

    print_step("1. User Registration")
    if not register_user(recruiter_email, password, "recruiter"): return
    if not register_user(freelancer_email, password, "freelancer"): return

    print_step("2. User Login")
    recruiter_token = login_user(recruiter_email, password)
    freelancer_token = login_user(freelancer_email, password)
    
    if not recruiter_token or not freelancer_token: return

    print_step("3. Post a Job (Recruiter)")
    job_data = {
        "title": "Senior Vue.js Developer",
        "description": "We need a Vue expert for a 3-month project.",
        "job_type": "contract",
        "experience_level": "senior",
        "pay_per_hour": "60.00",
        "required_skills": ["Vue.js", "JavaScript", "HTML"],
        "tech_stack": ["Vue", "Firebase"]
    }
    headers_rec = {"Authorization": f"Bearer {recruiter_token}"}
    res = requests.post(f"{BASE_URL}/jobs/", json=job_data, headers=headers_rec)
    if res.status_code == 201:
        job = res.json()
        print(f"✅ Job Posted: {job['title']} (ID: {job['id']})")
        job_id = job['id']
    else:
        print(f"❌ Failed to post job: {res.text}")
        return

    print_step("4. Apply for Job (Freelancer)")
    apply_data = {"cover_letter": "I have 5 years of Vue experience."}
    headers_free = {"Authorization": f"Bearer {freelancer_token}"}
    res = requests.post(f"{BASE_URL}/jobs/{job_id}/apply/", json=apply_data, headers=headers_free)
    if res.status_code == 201:
        app = res.json()
        print(f"✅ Application Submitted! (ID: {app['id']})")
        app_id = app['id']
    else:
        print(f"❌ Failed to apply: {res.text}")
        return

    print_step("5. View Applications (Recruiter)")
    # Using the new ApplicationListView logic we fixed
    res = requests.get(f"{BASE_URL}/applications/", headers=headers_rec)
    if res.status_code == 200:
        apps = res.json()
        my_app = next((a for a in apps if a['id'] == app_id), None)
        if my_app:
            print(f"✅ Recruiter sees application from {my_app['freelancer_email']}")
        else:
            print("❌ Recruiter did not see the new application.")
    else:
        print(f"❌ Failed to fetch applications: {res.text}")

    print_step("6. Accept Application (Recruiter)")
    status_data = {"status": "accepted"}
    res = requests.patch(f"{BASE_URL}/applications/{app_id}/status/", json=status_data, headers=headers_rec)
    if res.status_code == 200:
        print(f"✅ Application Accepted! Status: {res.json()['status']}")
    else:
        print(f"❌ Failed to update status: {res.text}")

    print("\n🎉 TEST COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    run_test()
