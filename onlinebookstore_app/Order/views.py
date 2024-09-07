from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import CustomerOrder, OrderDetail
from CustomerCartBook.models import CustomerCartBook
from Book.models import Book
from users.models import CustomUser as User

# insert new CustomerOrder(user_email) where PK index and order_code are genereated automatically, 
# at that time insert OrderDetail for all books in CustomerCartBook and delete all records in CustomerCartBook
@csrf_exempt
def insert_customer_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_email = data.get('user_email')
            user = User.objects.get(user_email=user_email)
            cart_items = CustomerCartBook.objects.filter(user_email__user_email=user_email)
            if not cart_items.exists():
                return JsonResponse({"message": "The cart is empty"}, status=400)
            
            # insert CustomerOrder
            customer_order = CustomerOrder.objects.create(user_email=user)

            # insert OrderDetail
            for cart_item in cart_items:
                book = Book.objects.get(book_name=cart_item.book_name)
                OrderDetail.objects.create(order_index=customer_order, book_name=book)

            # delete all records in CustomerCartBook
            cart_items.delete()
            return JsonResponse({"message": "Order placed successfully"}, status=201)
        except User.DoesNotExist:
            return JsonResponse({"message": "User does not exist"}, status=404)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

# query all CustomerOrder(user_email) records
@csrf_exempt
def query_customer_order(request):
    if request.method == "GET":
        try:
            user_email = request.GET.get('user_email')
            user = User.objects.get(user_email=user_email)
            customer_orders = CustomerOrder.objects.filter(user_email=user)
            order_codes = []
            for customer_order in customer_orders:
                order_codes.append(customer_order.order_code)
            return JsonResponse({"order_codes": order_codes}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"message": "User does not exist"}, status=404)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

# query all OrderDetail(order_code) records
@csrf_exempt
def query_order_detail(request):
    if request.method == "GET":
        try:
            order_code = request.GET.get('order_code')
            order = CustomerOrder.objects.get(order_code=order_code)
            order_details = OrderDetail.objects.filter(order_index__order_code=order_code)
            book_lists = [{
                "order_index": order_detail.order_index.order_index,
                "book_name": order_detail.book_name.book_name
            } for order_detail in order_details]
            return JsonResponse({"book_lists": book_lists}, status=200)
        except CustomerOrder.DoesNotExist:
            return JsonResponse({"message": "Order Code does not exist"}, status=404)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request method"}, status=405)