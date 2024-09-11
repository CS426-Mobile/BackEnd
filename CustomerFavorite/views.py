from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomerFavorite
from Book.models import Book
from User.models import CustomUser as User
import json

@csrf_exempt
def insert_customer_favorite(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_email = data.get('user_email')
            book_name = data.get('book_name')

            # Fetch user and book instances (assuming these are foreign keys)
            user = User.objects.get(user_email=user_email)
            book = Book.objects.get(book_name=book_name)

            # Check if the record already exists
            if CustomerFavorite.objects.filter(user_email=user, book_name=book).exists():
                return JsonResponse({"message": "The record already exists"}, status=400)

            # Insert the record
            CustomerFavorite.objects.create(user_email=user, book_name=book)
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

# delete a customer_favorite(user_email, book_name) record
@csrf_exempt
def delete_customer_favorite(request):
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            user_email = data.get('user_email')
            book_name = data.get('book_name')

            # Fetch user and book instances (assuming these are foreign keys)
            user = User.objects.get(user_email=user_email)
            book = Book.objects.get(book_name=book_name)

            # Check if the record exists
            if not CustomerFavorite.objects.filter(user_email=user, book_name=book).exists():
                return JsonResponse({"message": "The record does not exist"}, status=400)

            # Delete the record
            CustomerFavorite.objects.filter(user_email=user, book_name=book).delete()
            return JsonResponse({"message": "Record deleted successfully"}, status=200)

        except User.DoesNotExist:
            return JsonResponse({"message": "User not found"}, status=404)
        except Book.DoesNotExist:
            return JsonResponse({"message": "Book not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON format"}, status=408)
    return JsonResponse({"message": "Invalid request method"}, status=405)

# query all customer_favorite(user_email) records, return (book_name, author_name, book_image) of Book
@csrf_exempt
def query_customer_favorite(request):
    if request.method == "GET":
        try:
            user_email = request.GET.get('user_email')
            book_names = CustomerFavorite.objects.filter(user_email__user_email=user_email)
            response = []
            for book_name in book_names:
                book = Book.objects.get(book_name=book_name.book_name)
                response.append({
                    "book_name": book.book_name,
                    "author_name": book.author_name.author_name,
                    "book_image": book.book_image,
                    "average_rating": book.average_rating(),
                    "price": book.price
                })
            return JsonResponse(response, safe=False, status=200)
        except User.DoesNotExist:
            return JsonResponse({"message": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

# query whether (user_email, book_name) record exists
@csrf_exempt
def query_customer_favorite_exist(request):
    if request.method == "GET":
        try:
            user_email = request.GET.get('user_email')
            book_name = request.GET.get('book_name')
            user = User.objects.get(user_email=user_email)
            book = Book.objects.get(book_name=book_name)
            if CustomerFavorite.objects.filter(user_email=user, book_name=book).exists():
                return JsonResponse({"message": "The record exists"}, status=200)
            else:
                return JsonResponse({"message": "The record does not exist"}, status=404)
        except User.DoesNotExist:
            return JsonResponse({"message": "User not found"}, status=404)
        except Book.DoesNotExist:
            return JsonResponse({"message": "Book not found"}, status=404)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)