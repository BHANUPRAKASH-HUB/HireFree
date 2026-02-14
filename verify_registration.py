import requests
import time

BASE_URL = "http://127.0.0.1:8001/api"

def run():
    email = f"test_name_{int(time.time())}@example.com"
    password = "password123"
    first_name = "Alice"
    last_name = "Wonderland"
    
    print(f"Registering {email} with name {first_name} {last_name}...")
    res = requests.post(f"{BASE_URL}/auth/register/", json={
        "email": email, 
        "password": password, 
        "user_type": "freelancer",
        "first_name": first_name,
        "last_name": last_name
    })
    print(f"Register Status: {res.status_code}")
    if res.status_code != 201:
        print(f"Error: {res.text}")
        return

    print("Logging in to verify data...")
    res = requests.post(f"{BASE_URL}/auth/login/", json={
        "email": email, "password": password
    })
    token = res.json()['access']
    
    print("Fetching User Details...")
    res = requests.get(f"{BASE_URL}/users/me/", headers={'Authorization': f'Bearer {token}'})
    user = res.json()
    
    print(f"User Data: {user}")
    
    if user.get('first_name') == first_name and user.get('last_name') == last_name:
        print("SUCCESS: Name fields verified correctly.")
    else:
        print("FAILURE: Name fields mismatch.")

if __name__ == "__main__":
    run()
