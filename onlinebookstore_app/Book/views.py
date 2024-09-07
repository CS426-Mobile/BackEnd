from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Book
from datetime import date
from django.views.decorators.csrf import csrf_exempt
import json

# Query 10 books(book_name, author_name, book_image) from the database
@csrf_exempt
def get_10_books(request):
    if request.method == "GET":
        books = Book.objects.all()[:10]
        response = [
            {
                "book_name": book.book_name,
                "author_name": book.author_name.author_name,
                "book_image": book.book_image,
                "average_rating": book.average_rating(),
            } for book in books
        ]
        return JsonResponse(response, safe=False, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

# Query 20 books(book_name, author_name, book_image) from the database
@csrf_exempt
def get_20_books(request):
    if request.method == "GET":
        books = Book.objects.all()[:20]
        response = [
            {
                "book_name": book.book_name,
                "author_name": book.author_name.author_name,
                "book_image": book.book_image,
                "average_rating": book.average_rating(),
            } for book in books
        ]
        return JsonResponse(response, safe=False, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

# Query Book(BookName, AuthorName, BookImage):
# category_name
# rating_optional: 1, 2, 3, 4, 5, all
# price_optional: yes, no. if yes: 
#   price_min
#   price_max
# rating_sort: none, desc, asc
# price_sort: none, desc, asc 

@csrf_exempt
def get_books_by_category(request):
    if request.method == "GET":
        data = request.GET
        category_name = data.get('category_name', '')
        rating = data.get('rating_optional', 'all')
        price_optional = data.get('price_optional', 'no')
        price_min = data.get('price_min', 0)
        price_max = data.get('price_max', 99999999)
        rating_sort = data.get('rating_sort', 'none')
        price_sort = data.get('price_sort', 'none')


        # Filter by category
        if category_name == '':
            books = Book.objects.all()
        else:
            books = Book.objects.filter(category__category_name=category_name)

        # Filter by rating
        rating_ranges = {
            '1': (1, 1.5),
            '2': (1.5, 2.5),
            '3': (2.5, 3.5),
            '4': (3.5, 4.5),
            '5': (4.5, 5),
            'all': (1, 5),
        }
        # filter average rating whitin rating_ranges using book.average_rating(self)
        filtered_books = []
        for book in books:
            avg_rating = book.average_rating()
            if rating == 'all' or (rating in rating_ranges and rating_ranges[rating][0] <= avg_rating <= rating_ranges[rating][1]):
                filtered_books.append({
                    'book_name': book.book_name,
                    'author_name': book.author_name.author_name,
                    'book_image': book.book_image,
                    'average_rating': avg_rating,
                    'price': book.price,
                })

        # Sort by average rating
        if rating_sort != 'none':
            filtered_books.sort(key=lambda x: x['AverageRating'], reverse=(rating_sort == 'desc'))

        # Sort by price
        if price_sort != 'none':
            filtered_books.sort(key=lambda x: x['Price'], reverse=(price_sort == 'desc'))

        # Make return data
        result = [
            {
                'book_name': book['book_name'],
                'author_name': book['author_name'],
                'book_image': book['book_image'],
            } for book in filtered_books
        ]
        
        return JsonResponse(result, safe=False, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

# Query Book(BookName, AuthorName, BookImage) having book_input matching a part of book_name and combine similar to above
@csrf_exempt
def get_books_by_matching_string(request):
    if request.method == "GET":
        data = request.GET
        category_name = data.get('category_name', '')
        book_input = data.get('book_input', '')
        rating = data.get('rating_optional', 'all')
        price_optional = data.get('price_optional', 'no')
        price_min = data.get('price_min', 0)
        price_max = data.get('price_max', 99999999)
        rating_sort = data.get('rating_sort', 'none')
        price_sort = data.get('price_sort', 'none')

        # Filter by category
        if category_name == '':
            books = Book.objects.all()
        else:
            books = Book.objects.filter(category__category_name=category_name)

        # Filter by matching string
        books = books.filter(book_name__contains=book_input)

        # Filter by rating
        rating_ranges = {
            '1': (1, 1.5),
            '2': (1.5, 2.5),
            '3': (2.5, 3.5),
            '4': (3.5, 4.5),
            '5': (4.5, 5),
            'all': (1, 5),
        }
        # filter average rating whitin rating_ranges using book.average_rating(self)
        filtered_books = []
        for book in books:
            avg_rating = book.average_rating()
            if rating == 'all' or (rating in rating_ranges and rating_ranges[rating][0] <= avg_rating <= rating_ranges[rating][1]):
                filtered_books.append({
                    'book_name': book.book_name,
                    'author_name': book.author_name.author_name,
                    'book_image': book.book_image,
                    'average_rating': avg_rating,
                    'price': book.price,
                })

        # Sort by average rating
        if rating_sort != 'none':
            filtered_books.sort(key=lambda x: x['AverageRating'], reverse=(rating_sort == 'desc'))

        # Sort by price
        if price_sort != 'none':
            filtered_books.sort(key=lambda x: x['Price'], reverse=(price_sort == 'desc'))

        # Make return data
        result = [
            {
                'book_name': book['book_name'],
                'author_name': book['author_name'],
                'book_image': book['book_image'],
            } for book in filtered_books
        ]
        
        return JsonResponse(result, safe=False, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

# query all information of book_name
@csrf_exempt
def get_book_info(request, book_name):
    if request.method == "GET":
        book = Book.objects.filter(book_name=book_name).first()
        if book is None:
            return JsonResponse({"message": "Book not found"}, status=404)

        response = {
            "book_name": book.book_name,
            "author_name": book.author_name.author_name,
            "category": book.category.category_name,
            "book_image": book.book_image,
            "price": book.price,
            "num_1_star": book.num_1_star,
            "num_2_star": book.num_2_star,
            "num_3_star": book.num_3_star,
            "num_4_star": book.num_4_star,
            "num_5_star": book.num_5_star,
            "book_description": book.book_description,
            "public_date": book.public_date,
            "book_language": book.book_language,
            "book_weight": book.book_weight,
            "book_page": book.book_page,
            "average_rating": book.average_rating(),
        }
        return JsonResponse(response, safe=False, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

# query number of books of author_name
@csrf_exempt
def get_num_books(request, author_name):
    if request.method == "GET":
        num_books = Book.objects.filter(author_name=author_name).count()
        return JsonResponse({"num_books": num_books}, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

# query all category that author_name has written
@csrf_exempt
def get_author_categories(request, author_name):
    if request.method == "GET":
        books = Book.objects.filter(author_name=author_name)
        categories = set([book.category.category_name for book in books])
        return JsonResponse({"categories": list(categories)}, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

# query all books that have the same category with book_name
@csrf_exempt
def get_related_books(request, book_name):
    if request.method == "GET":
        book = Book.objects.filter(book_name=book_name).first()
        if book is None:
            return JsonResponse({"message": "Book not found"}, status=404)

        related_books = Book.objects.filter(category=book.category).exclude(book_name=book_name)
        response = [
            {
                "book_name": related_book.book_name,
                "author_name": related_book.author_name.author_name,
                "book_image": related_book.book_image
            } for related_book in related_books
        ]
        return JsonResponse(response, safe=False, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)