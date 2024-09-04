import requests
import json

URL = 'http://127.0.0.1:8000'
# URL = 'http://192.168.1.14:8000'

def test_register():
    url = URL + '/register/'
    data = {
        "email": "test@example.com",
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
        "email": "test@example.com",
        "password": "password321"
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
    url = URL + '/get_user_info/'
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers, cookies=cookies)

    print(f'Status Code: {response.status_code}')
    if response.status_code == 200:
        user_info = response.json().get("user", {})
        email = user_info.get("email", "No email found")
        print(f'Email: {email}')
    else:
        print('Failed to retrieve user information')

# get all User from the database db.sqlite3
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinebookstore_app.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def get_all_users():
    users = User.objects.all()
    for user in users:
        print(f'ID: {user.id}, Email: {user.email}, password: {user.password}')

def test_change_password(cookies):
    url = URL + '/change_password/'
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

def test_author_add():
    url = URL + '/author/'
    data = {
        "author_name": "John Doe 6",
        "num_follower": 100,
        "about": "A mysterious author",
        "image_url": "https://static.wikia.nocookie.net/villains/images/a/a0/John_Doe_game2.png"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.put(url, data=json.dumps(data), headers=headers)

    print(f'Status Code: {response.status_code}')
    if response.status_code == 201:
        print(f'Response JSON: {response.json()}')
    else:
        print(f'Response JSON: {response.json()}')

from django.core.files.temp import NamedTemporaryFile
import urllib.request
def download_test():
    url = 'https://static.wikia.nocookie.net/villains/images/a/a0/John_Doe_game.png'
    # response = requests.get(url)
    urllib.request.urlretrieve(url, 'E:/tmp2.png')
    # img_temp = NamedTemporaryFile(delete=True)
    # img_temp.write(response.content)
    # img_temp.flush()
    # return img_temp

def download_test2():
    url = 'https://static.wikia.nocookie.net/villains/images/a/a0/John_Doe_game.png'
    
    # Download the image from the URL
    response = requests.get(url)
    response.raise_for_status()  # Ensure we handle HTTP errors

    # Use NamedTemporaryFile with 'delete=False' to avoid issues with automatic deletion
    with NamedTemporaryFile(delete=False) as img_temp:
        img_temp.write(response.content)
        img_temp.flush()

    return img_temp

if __name__ == "__main__":
    # test_register()
    # cookies = test_login()
    # # test_getuserinfo(cookies)
    # test_change_password(cookies)
    # test_logout(cookies)
    # # test_getuserinfo(cookies)
    # test_logout(cookies)
    # get_all_users()
    test_author_add()
    download_test()
