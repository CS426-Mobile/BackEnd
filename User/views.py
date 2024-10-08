import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.utils import timezone
User = get_user_model()

@csrf_exempt
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_email = data.get("user_email")
        password = data.get("password")
        password2 = data.get("password2")

        if password != password2:
            return JsonResponse({"message": "Passwords do not match"}, status=400)
        
        if User.objects.filter(user_email=user_email).exists():
            return JsonResponse({"message": "Email is already taken"}, status=400)
        
        # Using the create_user method from CustomerManager
        user = User.objects.create_user(user_email=user_email, password=password)
        return JsonResponse({"message": "Account was created successfully"}, status=201)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_email = data.get("user_email")
        password = data.get("password")

        # Check if the email exists
        if not User.objects.filter(user_email=user_email).exists():
            return JsonResponse({"message": "User does not exist"}, status=400)

        # Authenticate the user
        user = authenticate(request, user_email=user_email, password=password)
        if user is None:
            return JsonResponse({"message": "Incorrect password"}, status=400)

        # Invalidate other sessions for this user before logging in
        user_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        for session in user_sessions:
            session_data = session.get_decoded()
            if session_data.get('_auth_user_id') == str(user.id):
                session.delete()

        # Log in the user and create a new session
        auth_login(request, user)
        return JsonResponse({"message": "Login successful"}, status=200)

    return JsonResponse({"message": "Invalid request method"}, status=405)

@csrf_exempt
@login_required
def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return JsonResponse({"message": "Logout successful"}, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

@login_required
def get_user_info_from_cookies(request):
    if request.method == "GET":
        user = request.user
        user_info = {
            "user_email": user.user_email,
            "address": user.user_address,
        }
        return JsonResponse({"user": user_info}, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)
    
@csrf_exempt
@login_required
def change_password(request):
    if request.method == "POST":
        data = json.loads(request.body)
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        new_password2 = data.get("new_password2")

        if new_password != new_password2:
            return JsonResponse({"message": "New passwords do not match"}, status=400)
        
        user = request.user
        if not user.check_password(old_password):
            return JsonResponse({"message": "Incorrect old password"}, status=400)
        
        user.set_password(new_password)
        user.save()
        return JsonResponse({"message": "Password changed successfully"}, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

@csrf_exempt
@login_required
def update_address(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_address = data.get("address")

        user = request.user
        user.user_user_address = user_address
        user.user_save()
        return JsonResponse({"message": "Address updated successfully"}, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

@csrf_exempt
@login_required
def update_address_with_email(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_email = data.get("user_email")
        user_address = data.get("address")

        user = User.objects.filter(user_email=user_email).first()
        if user is None:
            return JsonResponse({"message": "User does not exist"}, status=400)
        user.user_address = user_address
        user.save()
        return JsonResponse({"message": "Address updated successfully"}, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

# get address of user_email
def get_address(request, user_email):
    if request.method == "GET":
        user = User.objects.filter(user_email=user_email).first()
        if user is None:
            return JsonResponse({"message": "User does not exist"}, status=400)
        return JsonResponse({"address": user.user_address}, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)