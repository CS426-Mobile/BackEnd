from django.urls import path
from . import views

urlpatterns = [
    # Insert a new customer order
    path('order/insert/', views.insert_customer_order, name='insert_customer_order'),
    
    # Query all customer orders for a user
    path('order/query/', views.query_customer_order, name='query_customer_order'),
    
    # Query all order details for a specific order code
    path('order/detail/', views.query_order_detail, name='query_order_detail'),
]
