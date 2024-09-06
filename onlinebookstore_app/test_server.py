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

# URL = 'http://127.0.0.1:8000'
URL = 'http://192.168.72.150:8000'

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

def test_get_5_author():
    # path("author/popular_5/", views.get_5_popular_authors, name='get_5_popular_authors'),
    # def get_5_popular_authors(request):
    # if request.method == "GET":
    #     authors = Author.objects.order_by('-num_follower')[:5]

    #     authors_json = [
    #         {
    #             "author_name": author.author_name,
    #             "num_follower": author.num_follower,
    #             "about": author.about,
    #             "author_image": author.author_image
    #         }
    #         for author in authors
    #     ]
    #     return JsonResponse(authors_json, status=200)
    
    # return JsonResponse({"message": "Invalid request method"}, status=405)
    url = URL + '/author/popular_5/'
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)

    print(f'Status Code: {response.status_code}')
    if response.status_code == 200:
        authors = response.json()
        for author in authors:
            print(f'Author Name: {author.get("author_name", "No name")}')
            print(f'Number of Followers: {author.get("num_follower", "No followers")}')
            print(f'About: {author.get("about", "No about")}')
            print(f'Author Image: {author.get("author_image", "No image")}')
            print()
    else:
        print('Failed to get 5 authors')

if __name__ == "__main__":
    # test_register()
    # cookies = test_login()
    # # test_getuserinfo(cookies)
    # # test_change_password(cookies)
    # test_logout(cookies)
    # # test_getuserinfo(cookies)
    # test_logout(cookies)
    test_get_5_author()