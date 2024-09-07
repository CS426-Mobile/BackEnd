from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import json
from django.core.files.temp import NamedTemporaryFile
from .models import Author
from django.views.decorators.csrf import csrf_exempt
from .utils import ensure_image_exist

@csrf_exempt
def author(request):
    if request.method == "GET":
        author_name = request.GET.get('author_name')
        author = Author.objects.get(author_name=author_name)
        if author is None:
            return JsonResponse({"message": "Author not found"}, status=404)

        author_json = {
            "author_name": author.author_name,
            "num_follower": author.num_follower,
            "about": author.about,
            "author_image": author.author_image
        }
        return JsonResponse(author_json, safe=False, status=200)

    if request.method == "POST":
        data = json.loads(request.body)
        author_name = data.get("author_name")

        if Author.objects.filter(author_name=author_name).exists():
            return JsonResponse({"message": "Author already exists"}, status=400)
        
        num_follower = data.get("num_follower")
        about = data.get("about")
        author_image = data.get("author_image")
        author_image = ensure_image_exist(author_image)
        
        author = Author(author_name=author_name, num_follower=num_follower, about=about, author_image=author_image)
        author.save()
        return JsonResponse({"message": "Author created successfully"}, status=201)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)
    
@csrf_exempt
def all_authors(request):
    if request.method == "GET":
        authors = Author.objects.all()
        authors_json = [
            {
                "author_name": author.author_name,
                "num_follower": author.num_follower,
                "about": author.about,
                "author_image": author.author_image
            }
            for author in authors
        ]
        return JsonResponse(authors_json, safe=False, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

@csrf_exempt
def request_images(request, author_name):
    author = Author.objects.get(author_name=author_name)
    if author is None:
        return JsonResponse({"message": "Author not found"}, status=404)

    author_image = author.author_image
    return JsonResponse({"author_image": author_image}, status=200)

# Get 5 authors with the most followers
@csrf_exempt
def get_5_popular_authors(request):
    if request.method == "GET":
        authors = Author.objects.order_by('-num_follower')[:5]

        authors_json = [
            {
                "author_name": author.author_name,
                "num_follower": author.num_follower,
                "about": author.about,
                "author_image": author.author_image
            }
            for author in authors
        ]
        return JsonResponse(authors_json, safe=False, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

# Get author_name (author_name, author_image) from the database
@csrf_exempt
def get_simple_author(request):
    if request.method == "GET":
        author_name = request.GET.get('author_name', '')
        authors = Author.objects.get(author_name=author_name)

        if authors is None:
            return JsonResponse({"message": "Author not found"}, status=404)
        author_json = {
            "author_name": authors.author_name,
            "author_image": authors.author_image
        }
        return JsonResponse(author_json, safe=False, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

# Get match_string author_name (author_name, author_image) from the database
@csrf_exempt
def get_match_string_authors(request):
    if request.method == "GET":
        author_name = request.GET.get('author_name', '')
        authors = Author.objects.filter(author_name__icontains=author_name)
        authors_json = [
            {
                "author_name": author.author_name,
                "author_image": author.author_image
            }
            for author in authors
        ]
        return JsonResponse(authors_json, safe=False, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

# Get all info of an Author(author_name) from the database
@csrf_exempt
def get_author_info(request):
    if request.method == "GET":
        author_name = request.GET.get('author_name')
        author = Author.objects.get(author_name=author_name)
        if author is None:
            return JsonResponse({"message": "Author not found"}, status=404)

        author_json = {
            "author_name": author.author_name,
            "num_follower": author.num_follower,
            "about": author.about,
            "author_image": author.author_image
        }
        return JsonResponse(author_json, safe=False, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)