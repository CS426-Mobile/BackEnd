from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import CustomerOrder, OrderDetail
from CustomerCartBook.models import CustomerCartBook
from Book.models import Book
from User.models import CustomUser as User

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
                OrderDetail.objects.create(order_index=customer_order, book_name=book, num_books=cart_item.num_books)

            # delete all records in CustomerCartBook
            cart_items.delete()
            return JsonResponse({"message": "Order placed successfully"}, status=201)
        except User.DoesNotExist:
            return JsonResponse({"message": "User does not exist"}, status=404)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

# query all CustomerOrder(user_email) records, return list of orders including (order_code, total_price, num_books)
@csrf_exempt
def query_customer_order(request):
    if request.method == "GET":
        try:
            user_email = request.GET.get('user_email')
            orders = CustomerOrder.objects.filter(user_email__user_email=user_email)
            order_list = []
            for order in orders:
                order_details = OrderDetail.objects.filter(order_index__order_code=order.order_code)
                total_price = order.total_price()
                num_books = len(order_details)
                order_list.append({
                    "order_code": order.order_code,
                    "total_price": total_price,
                    "num_books": num_books
                })
            return JsonResponse({"order_list": order_list}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"message": "User does not exist"}, status=404)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request method"}, status=405)

# query all OrderDetail(order_code) records, return (order_code, Book(book_name, author_name, book_image, average_rating, price, num_books))
@csrf_exempt
def query_order_detail(request):
    if request.method == "GET":
        try:
            order_code = request.GET.get('order_code')
            order_details = OrderDetail.objects.filter(order_index__order_code=order_code)
            response = []
            for order_detail in order_details:
                book = Book.objects.get(book_name=order_detail.book_name)
                response.append({
                    "book_name": book.book_name,
                    "author_name": book.author_name.author_name,
                    "book_image": book.book_image,
                    "average_rating": book.average_rating(),
                    "price": book.price,
                    "num_books": order_detail.num_books
                })
            return JsonResponse(response, safe=False, status=200)
        except CustomerOrder.DoesNotExist:
            return JsonResponse({"message": "Order does not exist"}, status=404)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request method"}, status=405)