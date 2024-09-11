from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for inserting a new customer_cart_book record
    path('cart/insert/', views.insert_customer_cart_book, name='insert_customer_cart_book'),

    # URL pattern for deleting a customer_cart_book record
    path('cart/delete/', views.delete_customer_cart_book, name='delete_customer_cart_book'),

    # URL pattern for increasing the number of books in the cart by 1
    path('cart/increase/', views.increase_num_books, name='increase_num_books'),

    # URL pattern for decreasing the number of books in the cart by 1
    path('cart/decrease/', views.decrease_num_books, name='decrease_num_books'),

    # URL pattern for calculating the total price of the books in the cart for a user
    path('cart/total_price/', views.calculate_total_price, name='calculate_total_price'),

    # URL pattern for querying all customer_cart_book records for a user
    path('cart/query/', views.query_customer_cart_book, name='query_customer_cart_book'),
]
