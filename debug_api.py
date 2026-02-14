import requests
import json
import time

BASE_URL = "http://127.0.0.1:8001/api"

def print_res(name, res):
    print(f"--- {name} ---")
    print(f"Status: {res.status_code}")
    print(f"Body: {res.text[:300]}")
    print("----------------")

def run():
    # 1. Login as Recruiter
    email = f"recruiter_debug_{int(time.time())}@example.com"
    password = "password123"
    requests.post(f"{BASE_URL}/auth/register/", json={"email": email, "password": password, "user_type": "recruiter", "first_name": "Rec", "last_name": "Ruiter"})
    token = requests.post(f"{BASE_URL}/auth/login/", json={"email": email, "password": password}).json()['access']
    headers = {'Authorization': f'Bearer {token}'}

    # 2. Test Public Profile (for Chat) - Get OWN profile first to get ID
    user_id = requests.get(f"{BASE_URL}/users/me/", headers=headers).json()['id']
    print(f"Recruiter ID: {user_id}")
    
    # Try fetching public profile of self (should work if logic allows)
    res = requests.get(f"{BASE_URL}/users/{user_id}/", headers=headers)
    print_res("Public Profile Fetch", res)

    # 3. Test Job Post - Empty Tech Stack
    job_data_empty = {
        "title": "Job No Stack",
        "description": "Desc",
        "job_type": "full_time",
        "experience_level": "junior",
        "pay_per_hour": 50,
        "location": "Remote",
        "required_skills": ["Python"]
        # tech_stack missing
    }
    res = requests.post(f"{BASE_URL}/jobs/", json=job_data_empty, headers=headers)
    print_res("Job Post (No Tech Stack)", res)

    # 4. Test Job Post - With Tech Stack
    job_data_full = {
        "title": "Job With Stack",
        "description": "Desc",
        "job_type": "full_time",
        "experience_level": "junior",
        "pay_per_hour": 50,
        "location": "Remote",
        "required_skills": ["Python"],
        "tech_stack": ["Django"]
    }
    res = requests.post(f"{BASE_URL}/jobs/", json=job_data_full, headers=headers)
    print_res("Job Post (With Tech Stack)", res)

if __name__ == "__main__":
    run()
