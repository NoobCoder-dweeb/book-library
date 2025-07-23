from django.shortcuts import render, HttpResponse
from .models import Book

# Create your views here.
def home (request):
    # return HttpResponse("Hello, world! This is the home page of the online library.")
    return render(request, "home.html")

def books_list(request):
    books = Book.objects.all()
    # return render(request, "books_list.html", {"books": books})
    # return HttpResponse(f"Books list: {', '.join([book.title for book in books])}")
    book = books[0] if books else None
    print(book.pk == book.isbn)
    return HttpResponse(f"{book.author} - {book.title} - {book.isbn} - {book.pk}") if book else HttpResponse("No books available.")

def book_detail(request, book_id):
    book = Book.objects.get(isbn=book_id)
    # return HttpResponse(f"Book details: {book.title} by {book.author}")
    # return render(request, "book.html", {"book": book})