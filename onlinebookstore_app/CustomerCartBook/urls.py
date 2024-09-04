from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for inserting a new customer_cart_book record
    path('cart/insert/', views.insert_customer_cart_book, name='insert_customer_cart_book'),

    # URL pattern for deleting a customer_cart_book record
    path('cart/delete/', views.delete_customer_cart_book, name='delete_customer_cart_book'),

    # URL pattern for calculating the total price of the books in the cart for a user
    path('cart/total_price/', views.calculate_total_price, name='calculate_total_price'),
]
