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
# URL = 'http://192.168.72.150:8000'

def test_register():
    url = URL + '/register/'
    data = {
        "user_email": "test5@example.com",
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

def test_10_books():
    url = URL + '/books/20/'
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)

    print(f'Status Code: {response.status_code}')
    if response.status_code == 200:
        print(response.json())
    else:
        print('Failed to get 10 books')

def test_get_author():
    url = URL + '/author/'
    data = {
        "author_name": "Jeff Forcier"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers, params=data)

    print(f'Status Code: {response.status_code}')
    if response.status_code == 200:
        authors = response.json()
        print(authors)
    else:
        print('Failed to get authors')

def test_match_string_author():
    url = URL + '/author/match_string/'
    data = {
        "author_name": "Hoang"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers, params=data)

    print(f'Status Code: {response.status_code}')
    if response.status_code == 200:
        authors = response.json()
        for author in authors:
            print(f'Author Name: {author.get("author_name", "No name")}')
            print(f'Author Image: {author.get("author_image", "No image")}')
            print()
    else:
        print('Failed to get authors')

def test_get_books_by_matching_string():
    url = URL + '/books/matching_string/'
    data = {
        "book_input": "plica"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers, params=data)

    print(f'Status Code: {response.status_code}')
    if response.status_code == 200:
        books = response.json()
        for book in books:
            print(f'Book Name: {book.get("book_name", "No name")}')
            print(f'Author Name: {book.get("author_name", "No author")}')
            print(f'Book Image: {book.get("book_image", "No image")}')
            print()
    else:
        print('Failed to get books')
        
def test_get_related_books():
    book_name = "Python Web Development with Django"
    url = URL + f'/books/related/{book_name}/'
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)

    print(f'Status Code: {response.status_code}')
    if response.status_code == 200:
        books = response.json()
        for book in books:
            print(f'Book Name: {book.get("book_name", "No name")}')
            print(f'Author Name: {book.get("author_name", "No author")}')
            print(f'Book Image: {book.get("book_image", "No image")}')
            print()
    else:
        print(response.json())

def test_insert_customer_cart_book():
    # URL pattern for inserting a new customer_cart_book record
    # path('cart/insert/', views.insert_customer_cart_book, name='insert_customer_cart_book'),
    url = URL + '/cart/insert/'
    data = {
        "user_email": "user2@example.com",
        "book_name": "Python Web Development with Django"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    data2 = {
        "user_email": "user2@example.com",
        "book_name": "Programming in Python 3"
    }
    response2 = requests.post(url, data=json.dumps(data2), headers=headers)

    print(f'Status Code: {response.status_code}')

    if response.status_code == 201:
        print(f'Response JSON: {response.json()}')
    else:
        print('Failed to insert the record')

def test_calculate_total_price():
    # URL pattern for calculating the total price of the books in the cart for a user
    # path('cart/total_price/', views.calculate_total_price, name='calculate_total_price'),
    url = URL + '/cart/total_price/'
    data = {
        "user_email": "user2@example.com"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers, params=data)

    print(f'Status Code: {response.status_code}')

    if response.status_code == 200:
        total_price = response.json().get("total_price", "No total price")
        print(f'Total Price: {total_price}')

    else:
        print('Failed to calculate the total price')

def test_insert_customer_favorite():
    # URL pattern for inserting a new customer_favorite record
    # path('favorite/insert/', views.insert_customer_favorite, name='insert_customer_favorite'),
    url = URL + '/favorite/insert/'
    data = {
        "user_email": "user2@example.com",
        "book_name": "Python Web Development with Django"
        # "book_name": "Guangdong Wing Chun"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    print(f'Status Code: {response.status_code}')

    if response.status_code == 201:
        print(f'Response JSON: {response.json()}')
    else:
        print('Failed to insert the record')

def test_delete_customer_favorite():
    # URL pattern for deleting a customer_favorite record
    # path('favorite/delete/', views.delete_customer_favorite, name='delete_customer_favorite'),
    url = URL + '/favorite/delete/'
    data = {
        "user_email": "user2@example.com",
        "book_name": "Python Web Development with Django"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.delete(url, data=json.dumps(data), headers=headers)

    print(f'Status Code: {response.status_code}')

    if response.status_code == 200:
        print(f'Response JSON: {response.json()}')
    else:
        print('Failed to delete the record')

def test_query_customer_favorite():
    # URL pattern for querying all customer_favorite records for a user
    # path('favorite/query/', views.query_customer_favorite, name='query_customer_favorite'),
    url = URL + '/favorite/query/'
    data = {
        "user_email": "user2@example.com"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers, params=data)

    print(f'Status Code: {response.status_code}')

    if response.status_code == 200:
        books = response.json()
        for book in books:
            print(f'Book Name: {book.get("book_name", "No name")}')
            print(f'Author Name: {book.get("author_name", "No author")}')
            print(f'Book Image: {book.get("book_image", "No image")}')
            print()
    else:
        print(response.json())

def test_get_num_follower_from_customerfollow():
    # URL pattern for querying the number of followers a customer has in the CustomerFollow table
    # path('num_follower/customerfollow/', views.get_num_follower_from_customerfollow, name='get_num_follower_from_customerfollow'),
    url = URL + '/followers/author/count/'
    data = {
        "author_name": "Jeff Forcier"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers, params=data)  

    print(f'Status Code: {response.status_code}')
    print(f'Response JSON: {response.json()}')

def test_change_num_follower():
    # URL pattern for changing the number of followers an author has in the Author table
    # path('followers/author/change/', views.change_num_follower, name='change_num_follower'),
    url = URL + '/followers/author/change/'
    data = {
        "author_name": "Jeff Forcier",
        "change_num": 5
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    print(f'Status Code: {response.status_code}')
    print(f'Response JSON: {response.json()}')

def test_insert_customer_order():
    # URL pattern for inserting a new customer_order record
    # path('order/insert/', views.insert_customer_order, name='insert_customer_order'),
    url = URL + '/order/insert/'
    data = {
        "user_email": "user2@example.com"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    print(f'Status Code: {response.status_code}')
    print(f'Response JSON: {response.json()}')

def test_query_customer_order():
    # URL pattern for querying all customer_order records for a user
    # path('order/query/', views.query_customer_order, name='query_customer_order'),
    url = URL + '/order/query/'
    data = {
        "user_email": "user2@example.com"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers, params=data)

    print(f'Status Code: {response.status_code}')
    print(f'Response JSON: {response.json()}')

def test_query_order_detail():
    # URL pattern for querying all order_detail records for a specific order code
    # path('order/detail/', views.query_order_detail, name='query_order_detail'),
    url = URL + '/order/detail/'
    data = {
        "order_code": "P2az1F94aBrf"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers, params=data)

    print(f'Status Code: {response.status_code}')
    print(f'Response JSON: {response.json()}')

def post_func(url, data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(f'Status Code: {response.status_code}')
    print(f'Response JSON: {response.json()}')

if __name__ == "__main__":
    # test_register()
    # cookies = test_login()
    # # test_getuserinfo(cookies)
    # # test_change_password(cookies)
    # test_logout(cookies)
    # # test_getuserinfo(cookies)
    # test_logout(cookies)
    # test_get_5_author()
    # test_10_books()
    # test_match_string_author()
    # test_get_author()
    # test_get_books_by_matching_string()
    # test_insert_customer_cart_book()
    # # test_calculate_total_price()
    # # test_delete_customer_favorite()
    # # test_query_customer_favorite()
    # # test_get_num_follower_from_customerfollow()
    # # test_change_num_follower()
    # # test_insert_customer_favorite()
    # test_insert_customer_order()
    # test_query_customer_order()
    # test_query_order_detail()
    # test_get_author()
    # post_func(url="http://127.0.0.1:8000/cart/insert/", data={"user_email": "user2@example.com", "book_name": "Learning Swift"})
    # post_func(url="http://127.0.0.1:8000/cart/delete/", data={"user_email": "user2@example.com", "book_name": "Learning Swift"})
    post_func(url="http://127.0.0.1:8000/cart/increase/", data={"user_email": "user2@example.com", "book_name": "Learning Swift"})
    # post_func(url="http://127.0.0.1:8000/cart/decrease/", data={"user_email": "user2@example.com", "book_name": "Learning Swift"})