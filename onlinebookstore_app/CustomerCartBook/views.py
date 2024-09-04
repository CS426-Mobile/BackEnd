from django.shortcuts import render
from django.http import JsonResponse
from .models import CustomerCartBook
from django.views.decorators.csrf import csrf_exempt
from Book.models import Book
import json

# insert a new customer_cart_book(user_email, book_name) record
@csrf_exempt
def insert_customer_cart_book(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_email = data.get('user_email')
        book_name = data.get('book_name')
        # check if the record already exists
        if CustomerCartBook.objects.filter(user_email=user_email, book_name=book_name).exists():
            return JsonResponse({"message": "The record already exists"}, status=400)
        # insert the record
        CustomerCartBook.objects.create(user_email=user_email, book_name=book_name)
        return JsonResponse({"message": "Insert the record successfully"}, status=201)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

# delete a customer_cart_book(user_email, book_name) record
@csrf_exempt
def delete_customer_cart_book(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_email = data.get('user_email')
        book_name = data.get('book_name')
        # check if the record exists
        if not CustomerCartBook.objects.filter(user_email=user_email, book_name=book_name).exists():
            return JsonResponse({"message": "The record does not exist"}, status=400)
        # delete the record
        CustomerCartBook.objects.filter(user_email=user_email, book_name=book_name).delete()
        return JsonResponse({"message": "Delete the record successfully"}, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

# calculate the total price of the books in the cart of a user_email
@csrf_exempt
def calculate_total_price(request):
    if request.method == "GET":
        user_email = request.GET.get('user_email')
        book_names = CustomerCartBook.objects.filter(user_email=user_email)
        total_price = 0
        for book_name in book_names:
            total_price += Book.objects.get(book_name=book_name).price
        return JsonResponse({"total_price": total_price}, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)