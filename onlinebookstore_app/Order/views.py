from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import CustomerOrder, OrderDetail
from CustomerCartBook.models import CustomerCartBook
from Book.models import Book

# insert new CustomerOrder(user_email) where PK index and order_code are genereated automatically, 
# at that time insert OrderDetail for all books in CustomerCartBook and delete all records in CustomerCartBook
@csrf_exempt
def insert_customer_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_email = data.get('user_email')
        cart_items = CustomerCartBook.objects.filter(user_email=user_email)
        if not cart_items.exists():
            return JsonResponse({"message": "The cart is empty"}, status=400)
        
        # insert CustomerOrder
        customer_order = CustomerOrder.objects.create(user_email=user_email)

        # insert OrderDetail
        for cart_item in cart_items:
            book = Book.objects.get(book_name=cart_item.book_name)
            OrderDetail.objects.create(order_code=customer_order.order_code, book_name=cart_item.book_name, price=book.price)

        # delete all records in CustomerCartBook
        cart_items.delete()
        return JsonResponse({"message": "Order placed successfully"}, status=201)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

# query all CustomerOrder(user_email) records
@csrf_exempt
def query_customer_order(request):
    if request.method == "GET":
        user_email = request.GET.get('user_email')
        customer_orders = CustomerOrder.objects.filter(user_email=user_email)
        order_codes = []
        for customer_order in customer_orders:
            order_codes.append(customer_order.order_code)
        return JsonResponse({"order_codes": order_codes}, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

# query all OrderDetail(order_code) records
@csrf_exempt
def query_order_detail(request):
    if request.method == "GET":
        order_code = request.GET.get('order_code')
        order_details = OrderDetail.objects.filter(order_code=order_code)
        book_names = []
        prices = []
        for order_detail in order_details:
            book_names.append(order_detail.book_name)
            prices.append(order_detail.price)
        return JsonResponse({"book_names": book_names, "prices": prices}, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)