from django.shortcuts import render
from django.http import JsonResponse
from .models import Category
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def all_categories(request):
    if request.method == "GET":
        categories = Category.objects.all()
        response = [
            {
                "category_name": category.category_name
            } for category in categories
        ]
        return JsonResponse(response, safe=False)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)