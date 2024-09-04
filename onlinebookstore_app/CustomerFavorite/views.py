from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomerFavorite
from Book.models import Book
import json

# insert a new customer_favorite(user_email, book_name) record
@csrf_exempt
def insert_customer_favorite(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_email = data.get('user_email')
        book_name = data.get('book_name')
        # check if the record already exists
        if CustomerFavorite.objects.filter(user_email=user_email, book_name=book_name).exists():
            return JsonResponse({"message": "The record already exists"}, status=400)
        # insert the record
        CustomerFavorite.objects.create(user_email=user_email, book_name=book_name)
        return JsonResponse({"message": "Insert the record successfully"}, status=201)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

# delete a customer_favorite(user_email, book_name) record
@csrf_exempt
def delete_customer_favorite(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_email = data.get('user_email')
        book_name = data.get('book_name')
        # check if the record exists
        if not CustomerFavorite.objects.filter(user_email=user_email, book_name=book_name).exists():
            return JsonResponse({"message": "The record does not exist"}, status=400)
        # delete the record
        CustomerFavorite.objects.filter(user_email=user_email, book_name=book_name).delete()
        return JsonResponse({"message": "Delete the record successfully"}, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

# query all customer_favorite(user_email) records, return (book_name, author_name, book_image) of Book
@csrf_exempt
def query_customer_favorite(request):
    if request.method == "GET":
        user_email = request.GET.get('user_email')
        book_names = CustomerFavorite.objects.filter(user_email=user_email)
        response = []
        for book_name in book_names:
            book = Book.objects.get(book_name=book_name.book_name)
            response.append({
                "book_name": book.book_name,
                "author_name": book.author_name,
                "book_image": book.book_image
            })
        return JsonResponse(response, safe=False, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)