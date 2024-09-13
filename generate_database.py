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
from CustomerFollow.models import CustomerFollow
from CustomerFavorite.models import CustomerFavorite
from CustomerCartBook.models import CustomerCartBook

User = get_user_model()

def clean_database():
    Book.objects.all().delete()
    Category.objects.all().delete()
    Author.objects.all().delete()
    User.objects.all().delete()

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

def search_books(query, max_results=3):
    url = BOOKS_API_URL
    params = {
        'q': query,  # Câu truy vấn tìm kiếm (ví dụ: tên sách, tác giả)
        'key': API_KEY,
        'maxResults': max_results,
        'langRestrict': 'en'
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
        return []

def parse_published_date(date_str):
    try:
        # Try to parse full date (yyyy-mm-dd)
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except Exception as e:
        try:
            # Try to parse year only (yyyy)
            return datetime.strptime(date_str, '%Y').date().replace(month=1, day=1)
        except Exception as e:
            return datetime.strptime('2015-01-01', '%Y-%m-%d').date()
        
def insert_book_to_database(book):
    book_name = book.get('title', 'Unknown Title')
    author = book.get('authors', ['Unknown Author'])[0]
    category = book.get('categories', ['Unknown Category'])[0]
    book_image = book.get('imageLink', DEFAULT_NO_BOOK_IMAGE)
    public_date = parse_published_date(book.get('publishedDate', '2015-01-01'))

    # if books already exists, we skip
    if Book.objects.filter(book_name=book_name).exists():
        print(f'Book {book_name} already exists')
        return False

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
    return True

count_books = [0, 0, 0, 0]
books_added = {}
author_added = {}

def build_database_with_author(author, depth = 2):
    # We collect books from Google Books API
    books = search_books(author)
    count_books[depth] += len(books)
    print(f'count_books = {count_books}')
    for book in books:
        count_books[depth] -= 1
        # if book already exists, we skip
        if book.get('title') in books_added:
            continue
        insert_book_to_database(book)
        books_added.append(book.get('title'))
        # search author's books
        if depth > 0:
            author = book.get('authors', ['Unknown Author'])[0]
            if author in author_added:
                continue
            author_added[author] = True
            author_books = search_books(f"inauthor:{author}")
            count_books[depth] += len(author_books)
            # print number of books found
            for author_book in author_books:
                insert_book_to_database(author_book)
                author = author_book.get('authors', ['Unknown Author'])[0]
                build_database_with_author(author, depth - 1)

def collect_books_from_api():
    # We collect books from Google Books API
    titles = ['Fiction', 'Non-Fiction', 'Science Fiction', 'History', 'Psychology', 'Business', 'Children\'s Literature', 'Biography', 'Health', 'Education']
    entirebooks = []
    for title in titles:
        books = search_books(title)
        if books is not None:
            print(f'Found {len(books)} books for {title}')
            for book in books:
                entirebooks.append(book)
    return entirebooks

def build_database_with_authors(authors, depth = 2):
    # add author to author list
    author_lists = []
    author_added = {}
    for author in authors:
        if author in author_added:
            continue
        author_added[author] = True
        author_lists.append([author, depth])
    count_author = [0, 0, len(author_lists)]

    print_step = 0
    # bfs, while author_lists is not empty
    while len(author_lists) > 0:
        author, depth = author_lists.pop(0)
        count_author[depth] -= 1

        # We collect books from Google Books API
        books = search_books(author)
        count_author[depth] += len(books)
        for i in range(len(books)):
            book = books[i]
            if print_step == 0:
                print(f'Count Books = {count_books}')
            print_step = (print_step + 1) % 10
            insert_book_to_database(book)
            # search author's books
            if (depth > 0) and (i < 3):
                author = book.get('authors', ['Unknown Author'])[0]
                if author in author_added:
                    continue
                author_added[author] = True
                author_lists.append([author, depth - 1])
                count_author[depth] += 1

def generate_customerfollow():
    users = User.objects.all()
    authors = Author.objects.all()
    for i in range(0, 200):
        user = random.choice(users)
        author = random.choice(authors)
        print(f'Generating CustomerFollow {i}...')
        try:
            user = random.choice(users)
            author = random.choice(Author.objects.all())
            CustomerFollow.objects.create(
                user_email = user,
                author_name = author
            )
            print(f'CustomerFollow {i} was created successfully as {user} follows {author}')
        except Exception as e:
            print(f'Error creating CustomerFollow: {i}: {e}')

def generate_customerfavorite():
    users = User.objects.all()
    books = Book.objects.all()
    for i in range(0, 200):
        print(f'Generating CustomerFavorite {i}...')
        try:
            user = random.choice(users)
            book = random.choice(books)
            CustomerFavorite.objects.create(
                user_email = user,
                book_name = book
            )
            print(f'CustomerFavorite {i} was created successfully as {user} favorites {book}')
        except Exception as e:
            print(f'Error creating CustomerFavorite: {i}: {e}')

def generate_customercartbook():
    users = User.objects.all()
    books = Book.objects.all()
    for i in range(0, 200):
        print(f'Generating CustomerCartBook {i}...')
        try:
            user = random.choice(users)
            book = random.choice(books)
            CustomerCartBook.objects.create(
                user_email = user,
                book_name = book
            )
            print(f'CustomerCartBook {i} was created successfully as {user} adds {book} to cart')
        except Exception as e:
            print(f'Error creating CustomerCartBook: {i}: {e}')

def update_database():
    # We get all authors from the database
    authors = Author.objects.all()
    for author in authors:
        # We get all books from the database
        books = Book.objects.filter(author_name=author)
        print(f'Author {author.author_name}: {books.count()} books:')
        # get language of books
        languages = books.values('book_language').distinct()
        # if language not include 'vi', we skip
        if not any(language['book_language'] == 'vi' for language in languages):
            continue
        for book in books:
            print(f'    Book: {book.book_name}')
        # Get keyboard input, if 'y' then delete, otherwise skip
        delete_author = input('Do you want to delete this author? (y/n): ')
        if delete_author == 'y':
            # remove all books of this author from the database
            books.delete()
            # remove author from the database
            author.delete()
            print(f'Author {author.author_name} was deleted successfully')
        
def delete_author():
    author = input('Enter author name: ')
    try:
        author = Author.objects.get(author_name=author)
    except Author.DoesNotExist:
        print(f'Author {author} not found')
        return
    author_name = author.author_name
    books = Book.objects.filter(author_name=author)
    books.delete()
    author.delete()
    print(f'Author {author_name} was deleted successfully')

def collect_book_from_api_and_insert_book():
    # We collect books from Google Books API
    titles = ['Fiction', 'Non-Fiction', 'Science Fiction', 'History', 'Psychology', 'Business', 'Children\'s Literature', 'Biography', 'Health', 'Education']
    entirebooks = []
    for title in titles:
        books = search_books(title, max_results=30)
        if books is not None:
            print(f'Found {len(books)} books for {title}')
            for book in books:
                book.update({'categories': [title]})
                entirebooks.append(book)

    for book in entirebooks:
        insert_book_to_database(book)

def edit_all_price_star_weight_page():
    rating_possible = [1, 2, 3, 4, 5]
    weight_random_max = [1000, 500, 800, 1100, 8000]
    books = Book.objects.all()
    for book in books:
        # book.price = random.randint(20, 500) / 10.0
        # book.book_page = book.book_page if book.book_page > 0 else random.randint(20, 500)
        # book.book_weight = round(book.book_page * random.uniform(0.1175, 0.235), 2)

        weight_random = [random.randint(1, weight_random_max[i]) for i in range(5)]
        number_rating = random.randint(10, 5000)
        book.num_1_star = 0
        book.num_2_star = 0
        book.num_3_star = 0
        book.num_4_star = 0
        book.num_5_star = 0
        for _ in range(number_rating):
            rating = random.choices(rating_possible, weights=weight_random, k=1)[0]
            if rating == 1:
                book.num_1_star += 1
            elif rating == 2:
                book.num_2_star += 1
            elif rating == 3:
                book.num_3_star += 1
            elif rating == 4:
                book.num_4_star += 1
            else:
                book.num_5_star += 1
        book.save()
        print(f'Book {book.book_name} was updated successfully with average rating: {book.average_rating()}')

def edit_num_follower():
    authors = Author.objects.all()
    for author in authors:
        # count from CustomerFollow
        current_num_follower = CustomerFollow.objects.filter(author_name=author).count()
        # count average rating
        rating = author.average_rating()
        author.num_follower = random.randint(current_num_follower, current_num_follower + int(200 * rating))
        author.save()
        print(f'Author {author.author_name} was updated successfully with num_follower: {author.num_follower}')

def build_database_with_many_categories():
    if User.objects.all().count() == 0:
        generate_users()
    
    entirebooks = collect_books_from_api()
    authors = []
    count_books[-1] = len(entirebooks)
    for i in range(len(entirebooks)):
        book = entirebooks[i]
        insert_book_to_database(book)
        if i >= 3:
            continue
        author = book.get('authors', ['Unknown Author'])[0]
        authors.append(author)
    build_database_with_authors(authors)

    print("Database was built successfully")

def build_database():
    if User.objects.all().count() == 0:
        generate_users()
    collect_book_from_api_and_insert_book()
    edit_num_follower()
    edit_all_price_star_weight_page()
    generate_customerfollow()
    generate_customerfavorite()
    generate_customercartbook()

if __name__ == '__main__':
    build_database()