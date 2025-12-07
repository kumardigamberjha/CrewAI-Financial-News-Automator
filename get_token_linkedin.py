import requests
import string
import random
from urllib.parse import urlencode
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URL = os.getenv("LINKEDIN_REDIRECT_URI")


def generate_auth_url():
    base_url = "https://www.linkedin.com/oauth/v2/authorization"
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URL,
        "state": ''.join(random.choices(string.ascii_letters + string.digits, k=16)),
        "scope": "openid profile w_member_social",
    }

    return f"{base_url}?{urlencode(params)}"


def get_access_token(auth_code):
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = {
        "grant_type":"authorization_code",
        "code": auth_code,
        "redirect_uri" : REDIRECT_URL,
        "client_id" : CLIENT_ID,
        "client_secret" : CLIENT_SECRET,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)
    return response.json()


def get_user_id(access_token):
    url = "https://api.linkedin.com/v2/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()


if __name__ == "__main__":
    print("--- STEP 1: AUTHORIZE ---")
    print("Click this link to authorize your app:")
    print("-" * 20)
    print(generate_auth_url())
    print("-" * 20)
    
    print("\nAFTER you click 'Allow', look at the URL in your browser address bar.")
    print("It will look like: http://localhost:8000/callback?code=AQR_LONG_CODE_HERE&state=...")
    auth_code = input("\nCopy the 'code' part (everything between code= and &state) and paste it here: ")
    
    print("\n--- STEP 2: GENERATING TOKEN ---")
    token_data = get_access_token(auth_code)
    
    if "access_token" in token_data:
        print("\nSUCCESS! Here is your Access Token:")
        print("-" * 20)
        print(token_data["access_token"])
        print("-" * 20)
        print("\nNow paste this into your .env file as LINKEDIN_ACCESS_TOKEN")
        user_id = get_user_id(token_data["access_token"])
        print("User ID:", user_id)
        print("-" * 20)
        print("\nNow paste this into your .env file as LINKEDIN_USER_ID")

    else:
        print("\nERROR:")
        print(token_data)