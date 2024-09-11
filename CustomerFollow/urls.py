from django.urls import path
from . import views

urlpatterns = [
    path('followers/author/count_followtable/', views.get_num_follower_from_customerfollow, name='get_num_follower_from_customerfollow'),
    path('followers/author/count/', views.get_num_follower_from_author, name='get_num_follower_from_author'),
    path('followers/author/change/', views.change_num_follower, name='change_num_follower'),
    path('followers/author/query/', views.query_customer_follow, name='query_customer_follow'),
    path('followers/toggle/', views.toggle_follow, name='toggle_follow'),
    path('followers/query/', views.query_follow, name='query_follow'),
]
