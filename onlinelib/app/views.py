from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import Book
from django.db.models import Q
from django.views.decorators.http import require_GET
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create your views here.
def home (request):
    top_books = Book.objects.all().order_by("-rating").values()[:10]
    content = {
        "top_books": top_books,
        "title": "Online Library Home",
        "description": "Welcome to the Online Library. Explore our collection of books.",
        "keywords": "library, books, online, reading, literature",
    }
    # return HttpResponse("Hello, world! This is the home page of the online library.")
    return render(request, "home.html", content)

def about_us(request):
    content = {
        "title": "About Us",
        "description": "Learn more about our online library and our mission to promote reading.",
        "keywords": "about, online library, reading, books",
    }
    # return HttpResponse("This is the about us page of the online library.")
    return render(request, "about.html", content)

def contact(request):
    content = {
        "title": "Contact Us",
        "description": "Get in touch with us for any inquiries or support.",
        "keywords": "contact, online library, support, inquiries",
    }
    # return HttpResponse("This is the contact page of the online library.")
    return render(request, "contact.html", content) 

def books_list(request):
    books = Book.objects.all()
    if not books.exists():
        return HttpResponse("No books available.")
    
    return render(request, "books.html", {"books": books})

def book_detail(request, isbn):
    book = Book.objects.get(pk=isbn)
    return render(request, "book.html", {"book": book})

def search(request):
    # Access request to avoid unused parameter warning
    errors = []
    if request.method == "GET":
        if not request.GET.get("q"):
            errors.append("Please provide a book name to search.")
        else:
            name = request.GET.get("q", "").strip()
        
        if errors:
            return HttpResponse(" ".join(errors))
    
    name_pieces = name.split()
    query = Q()
    for piece in name_pieces:
        query |= Q(title__icontains=piece)
    books = Book.objects.filter(query)
    if not books.exists():
        return HttpResponse("No books found.")
    # return render(request, "search_results.html", {"books": books})
    return HttpResponse(f"Search results for '{name}': {', '.join([book.title for book in books])}")

@require_GET
@csrf_exempt  # remove if CSRF token is handled
def summarise(request):
    import requests
    import os
    import json

    title = request.GET.get('title', '')
    # API Configuration
    try:
        api_key = os.environ["LANGFLOW_API_KEY"]
    except KeyError:
        raise ValueError("LANGFLOW_API_KEY environment variable not found. Please set your API key in the environment variables.")

    url = "http://127.0.0.1:7860/api/v1/run/7d704b6f-8541-4865-8f77-ba720e1cd49f"  # The complete API endpoint URL for this flow

    # Request payload configuration
    payload = {
        "output_type": "chat",
        "input_type": "chat",
        "input_value": "Summarise the book titled: " + title,
    }

    # Request headers
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key  # Authentication key from environment variable
    }

    try:
        # Send API request
        response = requests.request("POST", url, json=payload, headers=headers)
        response.raise_for_status()  # Raise exception for bad status codes

        # Print response
        data = response.json()
        output = data["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
        summary = f"""This is a generated summary for the book: {title}.
        
        {output}"""
        return JsonResponse({'summary': summary})

    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error making API request: {e}")
    except ValueError as e:
        return HttpResponse(f"Error parsing response: {e}")
    
        
