from django.urls import path
from . import views

urlpatterns = [
    path('books/10/', views.get_10_books, name='get_10_books'),
    path('books/20/', views.get_20_books, name='get_20_books'),
    path('books/category/', views.get_books_by_category, name='get_books_by_category'),
    path('books/matching_category/', views.get_books_by_matching_string_category, name='get_books_by_matching_string_category'),
    path('book/<str:book_name>/', views.get_book_info, name='get_book_info'),
    path('books/author/<str:author_name>/count/', views.get_num_books, name='get_num_books'),
    path('books/author/<str:author_name>/categories/', views.get_author_categories, name='get_author_categories'),
    path('books/related/<str:book_name>/', views.get_related_books, name='get_related_books'),
]
