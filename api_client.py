import os
import httpx
from dotenv import load_dotenv
from cookies import Cache

load_dotenv()

API_BASE_URL = os.getenv('API_BASE_URL')
cache = Cache()

def refresh_and_retry(func, *args, **kwargs):
    try:
        response = func(*args, **kwargs)
        print(response.status_code)
        print(f"Before cookies: {cache.get_cookies()}")
        update_cookies(response)
        return response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            # If the middleware has already refreshed the tokens, try the request again
            response = func(*args, **kwargs)
            update_cookies(response)
            return response.json()
        else:
            raise e

def update_cookies(response):
    cookies = response.cookies
    if len(cookies) > 0:
        cache.set_cookies(cookies)
        print(f"!!!!!!!!!After cookies: {cache.get_cookies()}")
def add_infamy_bulk(data):
    return refresh_and_retry(_add_infamy_bulk, data)

def _add_infamy_bulk(data):
    url = f"{API_BASE_URL}/api/infamy/bulkAddInfamy"
    response = httpx.post(url, json=data, cookies=cache.get_cookies())
    response.raise_for_status()
    return response

def remove_infamy_bulk(data):
    return refresh_and_retry(_remove_infamy_bulk, data)

def _remove_infamy_bulk(data):
    url = f"{API_BASE_URL}/api/infamy/bulkRemoveInfamy"
    response = httpx.post(url, json=data, cookies=cache.get_cookies())
    response.raise_for_status()
    return response

def get_infamy(username):
    return refresh_and_retry(_get_infamy, username)

def _get_infamy(username):
    url = f"{API_BASE_URL}/api/infamy/getInfamy/{username}"
    response = httpx.get(url, cookies=cache.get_cookies())
    response.raise_for_status()
    return response

def get_top_infamy():
    return refresh_and_retry(_get_top_infamy)

def _get_top_infamy():
    url = f"{API_BASE_URL}/api/infamy/top"
    response = httpx.get(url, cookies=cache.get_cookies())
    response.raise_for_status()
    return response

def create_member(data):
    return refresh_and_retry(_create_member, data)

def _create_member(data):
    url = f"{API_BASE_URL}/api/member"
    response = httpx.post(url, json=data, cookies=cache.get_cookies())
    response.raise_for_status()
    return response

def get_user(username):
    return refresh_and_retry(_get_user, username)

def _get_user(username):
    url = f"{API_BASE_URL}/api/user"
    response = httpx.get(url, params={'name': username}, cookies=cache.get_cookies())
    response.raise_for_status()
    return response

def signup_user(data):
    url = f"{API_BASE_URL}/api/user/signup"
    response = httpx.post(url, json=data)
    response.raise_for_status()
    return response.json()

def login_user(data):
    url = f"{API_BASE_URL}/api/user/login"
    response = httpx.post(url, json=data)
    cookies = response.cookies
    cache.set_cookies(cookies)
    response.raise_for_status()
    return response.json()

def refresh_auth():
    url = f"{API_BASE_URL}/api/user/refresh"
    response = httpx.post(url, cookies=cache.get_cookies())
    response.raise_for_status()
    return response.json()

def logout_user():
    url = f"{API_BASE_URL}/api/user/logout"
    response = httpx.post(url, cookies=cache.get_cookies())
    response.raise_for_status()
    return response.json()