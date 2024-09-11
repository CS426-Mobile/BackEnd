from django.shortcuts import render
from django.http import JsonResponse
from .models import CustomerCartBook
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from Book.models import Book
import json

User = get_user_model()

# insert a new customer_cart_book(user_email, book_name) record
@csrf_exempt
def insert_customer_cart_book(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_email = data.get('user_email')
            book_name = data.get('book_name')

            # Fetch user and book instances (assuming these are foreign keys)
            user = User.objects.get(user_email=user_email)
            book = Book.objects.get(book_name=book_name)

            # Check if the record already exists
            if CustomerCartBook.objects.filter(user_email=user, book_name=book).exists():
                return JsonResponse({"message": "The record already exists"}, status=400)

            # Insert the record
            CustomerCartBook.objects.create(user_email=user, book_name=book)
            return JsonResponse({"message": "Record inserted successfully"}, status=201)

        except User.DoesNotExist:
            return JsonResponse({"message": "User not found"}, status=404)
        except Book.DoesNotExist:
            return JsonResponse({"message": "Book not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON format"}, status=408)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request method"}, status=405)

# delete a customer_cart_book(user_email, book_name) record
@csrf_exempt
def delete_customer_cart_book(request):
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            user_email = data.get('user_email')
            book_name = data.get('book_name')

            # Fetch user and book instances (assuming these are foreign keys)
            user = User.objects.get(user_email=user_email)
            book = Book.objects.get(book_name=book_name)

            # Check if the record exists
            if not CustomerCartBook.objects.filter(user_email=user, book_name=book).exists():
                return JsonResponse({"message": "The record does not exist"}, status=400)

            # Delete the record
            CustomerCartBook.objects.filter(user_email=user, book_name=book).delete()
            return JsonResponse({"message": "Record deleted successfully"}, status=200)

        except User.DoesNotExist:
            return JsonResponse({"message": "User not found"}, status=404)
        except Book.DoesNotExist:
            return JsonResponse({"message": "Book not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON format"}, status=408)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request method"}, status=405)

# increase the number of books in the cart of a CustomerCartBook(user_email, book_name) by 1
@csrf_exempt
def increase_num_books(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_email = data.get('user_email')
            book_name = data.get('book_name')

            # Fetch user and book instances (assuming these are foreign keys)
            user = User.objects.get(user_email=user_email)
            book = Book.objects.get(book_name=book_name)

            # If the record exists, create a new record
            if not CustomerCartBook.objects.filter(user_email=user, book_name=book).exists():
                CustomerCartBook.objects.create(user_email=user, book_name=book, num_books=0)

            # Increase the number of books by 1
            cart_book = CustomerCartBook.objects.get(user_email=user, book_name=book)
            cart_book.num_books += 1
            cart_book.save()
            return JsonResponse({"message": "Number of books increased successfully"}, status=200)

        except User.DoesNotExist:
            return JsonResponse({"message": "User not found"}, status=404)
        except Book.DoesNotExist:
            return JsonResponse({"message": "Book not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON format"}, status=408)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request method"}, status=405)

# decrease the number of books in the cart of a CustomerCartBook(user_email, book_name) by 1
@csrf_exempt
def decrease_num_books(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_email = data.get('user_email')
            book_name = data.get('book_name')

            # Fetch user and book instances (assuming these are foreign keys)
            user = User.objects.get(user_email=user_email)
            book = Book.objects.get(book_name=book_name)

            # Check if the record exists
            if not CustomerCartBook.objects.filter(user_email=user, book_name=book).exists():
                return JsonResponse({"message": "The record does not exist"}, status=400)

            # Decrease the number of books by 1
            cart_book = CustomerCartBook.objects.get(user_email=user, book_name=book)
            cart_book.num_books -= 1

            # If the number of books is 0, delete the record
            if cart_book.num_books == 0:
                cart_book.delete()
            else:
                cart_book.save()
            return JsonResponse({"message": "Number of books decreased successfully"}, status=200)

        except User.DoesNotExist:
            return JsonResponse({"message": "User not found"}, status=404)
        except Book.DoesNotExist:
            return JsonResponse({"message": "Book not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON format"}, status=408)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request method"}, status=405)

# calculate the total price of all books in the cart of a user_email
@csrf_exempt
def calculate_total_price(request):
    if request.method == "GET":
        user_email = request.GET.get('user_email')
        book_names = CustomerCartBook.objects.filter(user_email__user_email=user_email).values_list('book_name', flat=True)
        total_price = 0
        for book_name in book_names:
            total_price += Book.objects.get(book_name=book_name).price
        return JsonResponse({"total_price": total_price}, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

# query all customer_cart_book records for a user(user_email)
@csrf_exempt
def query_customer_cart_book(request):
    if request.method == "GET":
        user_email = request.GET.get('user_email')
        cart_books = CustomerCartBook.objects.filter(user_email__user_email=user_email)
        response = []
        for cart_book in cart_books:
            book = Book.objects.get(book_name=cart_book.book_name)
            response.append({
                "book_name": book.book_name,
                "author_name": book.author_name.author_name,
                "book_image": book.book_image,
                "average_rating": book.average_rating(),
                "price": book.price,
                "num_books": cart_book.num_books
            })
        return JsonResponse(response, safe=False, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)