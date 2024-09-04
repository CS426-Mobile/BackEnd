from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for inserting a new customer_favorite record
    path('favorite/insert/', views.insert_customer_favorite, name='insert_customer_favorite'),

    # URL pattern for deleting a customer_favorite record
    path('favorite/delete/', views.delete_customer_favorite, name='delete_customer_favorite'),

    # URL pattern for querying all customer_favorite records for a user
    path('favorite/query/', views.query_customer_favorite, name='query_customer_favorite'),
]
