from django.urls import path
from . import views

urlpatterns = [
    path("author/", views.author, name='author'),
    path("all_authors/", views.all_authors, name='all_authors'),
    path('author/<str:author_name>/image/', views.request_images, name='request_images'),
    path("author/popular_5/", views.get_5_popular_authors, name='get_5_popular_authors'),
    path("author/simple/", views.get_simple_authors, name='get_simple_authors'),
    path("author/match_string/", views.get_match_string_authors, name='get_matching_authors'),
    path("author/info/", views.get_author_info, name='get_author_info'),
]
