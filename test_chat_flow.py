import requests
import time

BASE_URL = "http://127.0.0.1:8000/api"

def register_user(email, password, user_type):
    url = f"{BASE_URL}/auth/register/"
    data = {"email": email, "password": password, "user_type": user_type}
    requests.post(url, json=data)

def login_user(email, password):
    url = f"{BASE_URL}/auth/login/"
    data = {"email": email, "password": password}
    res = requests.post(url, json=data)
    return res.json().get('access')

def run_chat_test():
    rec_email = f"rec_chat_{int(time.time())}@example.com"
    free_email = f"free_chat_{int(time.time())}@example.com"
    pwd = "password123"

    print("1. Registering Users...")
    register_user(rec_email, pwd, "recruiter")
    register_user(free_email, pwd, "freelancer")

    print("2. Logging In...")
    rec_token = login_user(rec_email, pwd)
    free_token = login_user(free_email, pwd)
    
    if not rec_token or not free_token:
        print("❌ Login failed")
        return

    # Get User IDs
    rec_user = requests.get(f"{BASE_URL}/users/me/", headers={"Authorization": f"Bearer {rec_token}"}).json()
    free_user = requests.get(f"{BASE_URL}/users/me/", headers={"Authorization": f"Bearer {free_token}"}).json()
    
    rec_id = rec_user['id']
    free_id = free_user['id']

    print("3. Sending Message (Recruiter -> Freelancer)...")
    msg_data = {"recipient": free_id, "content": "Hello Freelancer!"}
    res = requests.post(f"{BASE_URL}/messages/", json=msg_data, headers={"Authorization": f"Bearer {rec_token}"})
    if res.status_code == 201:
        print("✅ Message Sent!")
    else:
        print(f"❌ Failed to send message: {res.text}")
        return

    print("4. Retrieving Messages (Freelancer)...")
    res = requests.get(f"{BASE_URL}/messages/", headers={"Authorization": f"Bearer {free_token}"})
    msgs = res.json()
    
    if len(msgs) > 0 and msgs[0]['content'] == "Hello Freelancer!":
        print(f"✅ Freelancer received: '{msgs[0]['content']}' from {msgs[0]['sender_email']}")
    else:
        print(f"❌ Message not received. Response: {msgs}")

if __name__ == "__main__":
    run_chat_test()
