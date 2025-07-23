from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("books/", views.books_list, name="books_list"),
    path("books/{book_id}", views.book_detail, name="book_detail"),
]