from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name='register'),
    path("login/", views.login, name='login'),
    path("logout/", views.logout, name='logout'),
    path("user/get_user_info_from_cookies/", views.get_user_info_from_cookies, name='get_user_info'),
    path("user/change_password/", views.change_password, name='change_password'),
    path("user/update_address/", views.update_address, name='update_address'),
    path("user/update_address_with_email/", views.update_address_with_email, name='update_address_with_email'),
    path("user/get_address/", views.get_address, name='get_address'),
]
