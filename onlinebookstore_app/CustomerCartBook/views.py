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