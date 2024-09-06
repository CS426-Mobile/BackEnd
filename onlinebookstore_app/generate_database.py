import os
import django
import requests
import random
from django.contrib.auth import get_user_model
from datetime import datetime

BOOKS_API_URL = 'https://www.googleapis.com/books/v1/volumes'
AUTHORS_API_URL = 'https://www.wikidata.org/w/api.php'
API_KEY = 'AIzaSyBI7GKsq2l40OOPmRdDy4hxxx6LUIQuPkM'
DEFAULT_NO_BOOK_IMAGE = 'https://www.peeters-leuven.be/covers/no_cover.gif'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinebookstore_app.settings')
django.setup()

from Book.models import Book
from Author.models import Author
from Category.models import Category

User = get_user_model()

def generate_users():
    for i in range(0, 31):
        try:
            data = {
                "user_email": "user" + str(i) + "@example.com",
                "password": "123456",
                "user_address": "Ha Noi, Viet Nam"
            }
            user = User.objects.create_user(**data)
            print(f'User {user.user_email} was created successfully')
        except Exception as e:
            print(f'Error creating user: {i}: {e}')

def clean_database():
    User.objects.all().delete()
    Book.objects.all().delete()
    Author.objects.all().delete()

def find_wikipedia_page(title):
    # Tìm kiếm trang trên Wikipedia
    search_url = f'https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={title}&format=json'
    response = requests.get(search_url)
    
    if response.status_code == 200:
        data = response.json()
        search_results = data.get('query', {}).get('search', [])
        
        if search_results:
            # Trả về tiêu đề của trang đầu tiên tìm thấy
            page_title = search_results[0].get('title')
            return page_title
        else:
            return None
    else:
        print(f"Error fetching data from Wikipedia search API: {response.status_code}")
        return None

def get_wikipedia_summary(title):
    # Lấy tóm tắt từ tiêu đề của trang
    summary_url = f'https://en.wikipedia.org/api/rest_v1/page/summary/{title}'
    response = requests.get(summary_url)
    
    if response.status_code == 200:
        data = response.json()
        summary = data.get('extract', 'No summary available')
        image_url = data.get('thumbnail', {}).get('source', 'https://miamistonesource.com/wp-content/uploads/2018/05/no-avatar-25359d55aa3c93ab3466622fd2ce712d1.jpg')
        return summary, image_url
    else:
        print(f"Error fetching data from Wikipedia API: {response.status_code}")
        return None, None

def collect_author_from_api(author_name):
    page_title = find_wikipedia_page(author_name)
    if page_title:
        summary, image_url = get_wikipedia_summary(page_title)
    else:
        summary, image_url = 'No summary available', 'https://miamistonesource.com/wp-content/uploads/2018/05/no-avatar-25359d55aa3c93ab3466622fd2ce712d1.jpg'

    Author.objects.create(
        author_name = author_name,
        num_follower = random.randint(0, 1000),
        about = summary,
        author_image = image_url
    )
    print(f'Author {author_name} was created successfully')

def search_books(query, max_results=10):
    url = BOOKS_API_URL
    params = {
        'q': query,  # Câu truy vấn tìm kiếm (ví dụ: tên sách, tác giả)
        'key': API_KEY,
        'maxResults': max_results
    }
    
    # Gửi yêu cầu đến Google Books API
    response = requests.get(url, params=params)
    
    # Kiểm tra nếu yêu cầu thành công
    if response.status_code == 200:
        books = response.json().get('items', [])
        book_data = []
        for book in books:
            volume_info = book.get('volumeInfo', {})
            book_info = {
                'title': volume_info.get('title', 'No title'),
                'authors': volume_info.get('authors', 'No author'),
                'publisher': volume_info.get('publisher', 'No publisher'),
                'publishedDate': volume_info.get('publishedDate', '2015-01-01'),
                'description': volume_info.get('description', 'No description available'),
                'pageCount': volume_info.get('pageCount', 5),
                'categories': volume_info.get('categories', 'N/A'),
                'averageRating': volume_info.get('averageRating', 'N/A'),
                'ratingsCount': volume_info.get('ratingsCount', 'N/A'),
                'language': volume_info.get('language', 'N/A'),
                'imageLink': volume_info.get('imageLinks', {}).get('thumbnail', DEFAULT_NO_BOOK_IMAGE),
                'listPrice': volume_info.get('retailPrice', {}).get('amount', 10)
            }
            book_data.append(book_info)
        return book_data
    else:
        print(f"Error fetching data from Google Books API: {response.status_code}")
        return None

def parse_published_date(date_str):
    try:
        # Try to parse full date (yyyy-mm-dd)
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:    
        try:
            # Try to parse year only (yyyy)
            return datetime.strptime(date_str, '%Y').date().replace(month=1, day=1)
        except ValueError:
            return None
        
def collect_books_from_api():
    # We collect books from Google Books API
    titles = ['Python', 'Django', 'Java', 'JavaScript', 'React', 'Vue.js', 'Angular', 'Node.js', 'MongoDB', 'PostgreSQL']
    for title in titles:
        books = search_books(title, max_results=5)
        for book in books:
            book_name = book.get('title', 'Unknown Title')
            author = book.get('authors', ['Unknown Author'])[0]
            category = book.get('categories', ['Unknown Category'])[0]
            book_image = book.get('imageLink', DEFAULT_NO_BOOK_IMAGE)
            public_date = parse_published_date(book.get('publishedDate', '2015-01-01'))

            # if books already exists, we skip
            if Book.objects.filter(book_name=book_name).exists():
                print(f'Book {book_name} already exists')
                continue

            # if author not exists, we collect author from Wikipedia API
            if not Author.objects.filter(author_name=author).exists():
                collect_author_from_api(author)

            # if category not exists, we create new category
            if not Category.objects.filter(category_name=category).exists():
                Category.objects.create(category_name=category)
                print(f'Category {category} was created successfully')
            
            Book.objects.create(
                book_name = book_name,
                book_image = book_image,
                author_name = Author.objects.get(author_name=author),
                category = Category.objects.get(category_name=category),
                price = random.randint(1, 1000) / 10.0,
                num_1_star = random.randint(0, 100),
                num_2_star = random.randint(0, 100),
                num_3_star = random.randint(0, 100),
                num_4_star = random.randint(0, 100),
                num_5_star = random.randint(0, 100),
                book_description = book.get('description', 'No description available'),
                public_date = public_date,
                book_language = book.get('language', 'Unknown Language'),
                book_weight = round(book.get('pageCount', 0) * random.uniform(0.1175, 0.235), 2),
                book_page = book.get('pageCount', 0)
            )

            print(f'Book {book_name} was created successfully')

if User.objects.all().count() == 0:
    generate_users()

collect_books_from_api()