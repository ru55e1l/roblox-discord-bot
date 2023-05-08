# main.py
import bot
import os
from dotenv import load_dotenv
from api_client import login_user

def login_to_api():
    load_dotenv()
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    response = login_user({'username': username, 'password': password})
    if response.get('message') == 'Login successful':
        print("Login to API successful")
    else:
        print("Failed to log in to API")

if __name__ == '__main__':
    login_to_api()
    bot.run_discord_bot()
