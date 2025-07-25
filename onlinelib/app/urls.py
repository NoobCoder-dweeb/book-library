from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("books/", views.books_list, name="books_list"),
    path("about/", views.about_us, name="about"),
    path("contact/", views.contact, name="contact"),
    path("search/<str:title>/", views.search, name="search"),
    path("books/<int:book_id>/", views.book_detail, name="book_detail"),
]