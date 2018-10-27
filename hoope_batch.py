'''
Created on 2018/10/27

@author: Administrator
'''
import os
import requests
import dotenv
from bs4 import BeautifulSoup

def login_to_homelog():
    url = os.environ.get("URL")
    login_url = os.environ.get("LOGIN_URL")
    datasheet = os.environ.get("DATA_URL")
    user_id = os.environ.get("USER_ID")
    password = os.environ.get("PASSWORD")

    login_payload = {"utf-8": "✓", "admin_admin_user[email]":user_id, "admin_admin_user[password]":password}

    session = requests.Session()
    r = session.get(url)
    soup = BeautifulSoup(r.text, features='html.parser')
    auth_token = soup.find(attrs={'name': 'authenticity_token'}).get('value')
    login_payload['authenticity_token'] = auth_token

    session.post(login_url, data=login_payload)
    sheet_payload = {"utf-8": "✓", 'authenticity_token': auth_token, "month": "2018/09", "type": "1", "badgetype": "1"}
    response = session.post(datasheet, data=sheet_payload)
    print(response.content)

if __name__ == '__main__':
    print("start")
    login_to_homelog()
    print("end")
