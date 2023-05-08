import os
import httpx
from dotenv import load_dotenv
from cookies import Cache

load_dotenv()

API_BASE_URL = os.getenv('API_BASE_URL')
cache = Cache()

def add_infamy_bulk(data):
    url = f"{API_BASE_URL}/api/infamy/bulkAddInfamy"
    response = httpx.post(url, json=data, cookies=cache.get_cookies())
    return response.json()

def remove_infamy_bulk(data):
    url = f"{API_BASE_URL}/api/infamy/bulkRemoveInfamy"
    response = httpx.post(url, json=data, cookies=cache.get_cookies())
    return response.json()

def get_infamy(username):
    url = f"{API_BASE_URL}/api/infamy/getInfamy/{username}"
    response = httpx.get(url, cookies=cache.get_cookies())
    return response.json()

def get_top_infamy():
    url = f"{API_BASE_URL}/api/infamy/top"
    response = httpx.get(url, cookies=cache.get_cookies())
    return response.json()

def create_member(data):
    url = f"{API_BASE_URL}/api/member"
    response = httpx.post(url, json=data, cookies=cache.get_cookies())
    return response.json()

def get_user(username):
    url = f"{API_BASE_URL}/api/user"
    response = httpx.get(url, params={'name': username}, cookies=cache.get_cookies())
    return response.json()

def signup_user(data):
    url = f"{API_BASE_URL}/api/user/signup"
    response = httpx.post(url, json=data)
    return response.json()

def login_user(data):
    url = f"{API_BASE_URL}/api/user/login"
    response = httpx.post(url, json=data)
    cookies = response.cookies
    cache.set_cookies(cookies)
    return response.json()

def refresh_auth():
    url = f"{API_BASE_URL}/api/user/refresh"
    response = httpx.post(url, cookies=cache.get_cookies())
    return response.json()

def logout_user():
    url = f"{API_BASE_URL}/api/user/logout"
    response = httpx.post(url, cookies=cache.get_cookies())
    return response.json()
