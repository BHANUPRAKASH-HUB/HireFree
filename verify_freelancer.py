import requests
import time

BASE_URL = "http://127.0.0.1:8001/api"

def run():
    email = f"freelancer_test_{int(time.time())}@example.com"
    password = "password123"
    
    print(f"Registering {email}...")
    res = requests.post(f"{BASE_URL}/auth/register/", json={
        "email": email, "password": password, "user_type": "freelancer"
    })
    print(f"Register Status: {res.status_code}")
    
    if res.status_code == 201:
        print("Logging in...")
        res = requests.post(f"{BASE_URL}/auth/login/", json={
            "email": email, "password": password
        })
        print(f"Login Status: {res.status_code}")
        if res.status_code == 200:
            print("Login Success")
            token = res.json()['access']
            print(f"Token received: {token[:10]}...")
            
            # Try profile update
            headers = {'Authorization': f'Bearer {token}'}
            print("Updating profile...")
            res = requests.put(f"{BASE_URL}/users/profile/", json={
                "skills": ["A"], "tech_stack": ["B"], "hourly_rate": 10
            }, headers=headers)
            print(f"Profile Update Status: {res.status_code}")
            print(res.text)

if __name__ == "__main__":
    run()
