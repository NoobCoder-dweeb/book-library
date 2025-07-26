from django.shortcuts import render, HttpResponse
from .models import Book
from django.db.models import Q

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
    # return render(request, "books_list.html", {"books": books})
    # return HttpResponse(f"Books list: {', '.join([book.title for book in books])}")
    book = books[0] if books else None
    return HttpResponse(f"{book.author} - {book.title} - {book.isbn} - {book.pk}") if book else HttpResponse("No books available.")

def book_detail(request, book_id):
    book = Book.objects.get(pk=book_id)
    # return HttpResponse(f"Book details: {book.title} by {book.author}")
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