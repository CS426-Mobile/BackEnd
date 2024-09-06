import requests
import json

# get all User from the database db.sqlite3
import os
import django
# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinebookstore_app.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

URL = 'http://127.0.0.1:8000'
# URL = 'http://192.168.1.14:8000'

def test_register():
    url = URL + '/register/'
    data = {
        "user_email": "test1@example.com",
        "password": "password123",
        "password2": "password123"
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers)

    print(f'Status Code: {response.status_code}')
    print(f'Response JSON: {response.json()}')

# test login with that data
def test_login():
    url = URL + '/login/'
    data = {
        "user_email": "test1@example.com",
        "password": "password123"
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers)

    print(f'Status Code: {response.status_code}')
    print(f'Response JSON: {response.json()}')
    print (f'Cookies: {response.cookies}')
    return response.cookies

# test logout
def test_logout(cookies):
    url = URL + '/logout/'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, cookies=cookies)

    print(f'Status Code: {response.status_code}')
    if response.status_code == 200:
        print(f'Response JSON: {response.json()}')
    else:
        print('Failed to logout')
def test_getuserinfo(cookies):
    url = URL + '/user/get_user_info/'
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers, cookies=cookies)

    print(f'Status Code: {response.status_code}')
    if response.status_code == 200:
        user_info = response.json().get("user", {})
        email = user_info.get("email", "No email found")
        print(f'Email: {email}')
    else:
        print('Failed to retrieve user information')


def get_all_users():
    users = User.objects.all()
    for user in users:
        print(f'ID: {user.id}, Email: {user.user_email}, password: {user.password}')

def test_change_password(cookies):
    url = URL + '/user/change_password/'
    data = {
        "old_password": "password123",
        "new_password": "password321",
        "new_password2": "password321"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers, cookies=cookies)

    print(f'Status Code: {response.status_code}')
    if response.status_code == 200:
        print(f'Response JSON: {response.json()}')
    else:
        print('Failed to change password')

if __name__ == "__main__":
    test_register()
    cookies = test_login()
    # test_getuserinfo(cookies)
    # test_change_password(cookies)
    test_logout(cookies)
    # test_getuserinfo(cookies)
    test_logout(cookies)