from django.shortcuts import render
from .models import CustomerFollow
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Author.models import Author
from User.models import CustomUser as User
import json

# Query the number of followers of an author (author_name) in the CustomerFollow table
@csrf_exempt
def get_num_follower_from_customerfollow(request):
    if request.method == "GET":
        author_name = request.GET.get('author_name')
        num_follower = CustomerFollow.objects.filter(author_name__author_name=author_name).count()

        return JsonResponse({"num_follower": num_follower}, status=200)

    return JsonResponse({"message": "Invalid request method"}, status=405)

# Query the number of followers of an author (author) in the Author table
@csrf_exempt
def get_num_follower_from_author(request):
    if request.method == "GET":
        author_name = request.GET.get('author_name')
        try:
            author = Author.objects.get(author_name=author_name)
            num_follower = author.num_follower
            return JsonResponse({"num_follower": num_follower}, status=200)
        except Author.DoesNotExist:
            return JsonResponse({"message": "Author not found"}, status=404)

    return JsonResponse({"message": "Invalid request method"}, status=405)

# Change the number of followers of an author (from the Author table)
@csrf_exempt
def change_num_follower(request):
    if request.method == "POST":
        data = json.loads(request.body)
        author_name = data.get('author_name')
        change_num = data.get('change_num')
        try:
            author = Author.objects.get(author_name=author_name)
            author.num_follower += change_num
            author.save()
            return JsonResponse({"message": "Number of followers updated"}, status=200)
        except Author.DoesNotExist:
            return JsonResponse({"message": "Author not found"}, status=404)
        
    return JsonResponse({"message": "Invalid request method"}, status=405)

# Query all Author(author_name, author_image, num_follower) objects that a user(user_email) follows
@csrf_exempt
def query_customer_follow(request):
    if request.method == "GET":
        try:
            user_email = request.GET.get('user_email')
            authors = Author.objects.filter(customerfollow__user_email__user_email=user_email).values('author_name', 'author_image', 'num_follower')
            return JsonResponse(list(authors), safe=False, status=200)
        except Author.DoesNotExist:
            return JsonResponse({"message": "Author not found"}, status=404)

    return JsonResponse({"message": "Invalid request method"}, status=405)

# Query toggle follow status of an author (author_name) for a user (user_email), and update the number of followers of the author
@csrf_exempt
def toggle_follow(request):
    if request.method == "POST":
        data = json.loads(request.body)
        author_name = data.get('author_name')
        user_email = data.get('user_email')
        try:
            author = Author.objects.get(author_name=author_name)
            user = User.objects.get(user_email=user_email)
            follow = CustomerFollow.objects.filter(author_name__author_name=author_name, user_email__user_email=user_email)
            if follow.exists():
                follow.delete()
                author.num_follower -= 1
                author.save()
                return JsonResponse({"message": "Unfollowed"}, status=200)
            else:
                CustomerFollow.objects.create(author_name=author, user_email=user)
                author.num_follower += 1
                author.save()
                return JsonResponse({"message": "Followed"}, status=200)
        except Author.DoesNotExist:
            return JsonResponse({"message": "Author not found"}, status=404)
        except User.DoesNotExist:
            return JsonResponse({"message": "User not found"}, status=404)

    return JsonResponse({"message": "Invalid request method"}, status=405)

# Query follow status of an author (author_name) for a user (user_email)
@csrf_exempt
def query_follow(request):
    if request.method == "GET":
        author_name = request.GET.get('author_name')
        user_email = request.GET.get('user_email')
        try:
            follow = CustomerFollow.objects.filter(author_name__author_name=author_name, user_email__user_email=user_email)
            if follow.exists():
                return JsonResponse({"follow": True}, status=200)
            else:
                return JsonResponse({"follow": False}, status=200)
        except Author.DoesNotExist:
            return JsonResponse({"message": "Author not found"}, status=404)
        except User.DoesNotExist:
            return JsonResponse({"message": "User not found"}, status=404)

    return JsonResponse({"message": "Invalid request method"}, status=405)