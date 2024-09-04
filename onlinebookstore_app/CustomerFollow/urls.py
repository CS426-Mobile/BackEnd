from django.urls import path
from . import views

urlpatterns = [
    path('followers/customer/', views.get_num_follower_from_customerfollow, name='get_num_follower_from_customerfollow'),
    path('followers/author/', views.get_num_follower_from_author, name='get_num_follower_from_author'),
    path('followers/author/change/', views.change_num_follower, name='change_num_follower'),
]
