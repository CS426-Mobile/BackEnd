from django.shortcuts import render
from .models import CustomerFollow
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Author.models import Author
import json

# Query the number of followers a customer has in the CustomerFollow table
@csrf_exempt
def get_num_follower_from_customerfollow(request):
    if request.method == "GET":
        customer_name = request.GET.get('customer_name')
        num_follower = CustomerFollow.objects.filter(customer_name=customer_name).count()

        return JsonResponse({"num_follower": num_follower}, status=200)

    return JsonResponse({"message": "Invalid request method"}, status=405)

# Query the number of followers of an author (from the Author table)
@csrf_exempt
def get_num_follower_from_author(request):
    if request.method == "GET":
        customer_name = request.GET.get('customer_name')
        try:
            author = Author.objects.get(author_name=customer_name)
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
        customer_name = data.get('customer_name')
        change_num = data.get('change_num')

        try:
            author = Author.objects.get(author_name=customer_name)
            # Ensure followers count doesn't go negative
            author.num_follower = max(0, author.num_follower + change_num)  
            author.save()

            return JsonResponse({"message": "Change the number of followers successfully"}, status=200)
        except Author.DoesNotExist:
            return JsonResponse({"message": "Author not found"}, status=404)

    return JsonResponse({"message": "Invalid request method"}, status=405)