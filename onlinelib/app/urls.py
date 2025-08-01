from django.urls import path
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns = [
    path("", views.home, name="home"),
    path("books/", views.books_list, name="books_list"),
    path("about/", views.about_us, name="about"),
    path("contact/", views.contact, name="contact"),
    path("search/", views.search, name="search"),
    path("summarise/<str:book_title>", views.summarise, name="summarise"),
    path("books/<str:isbn>/", views.book_detail, name="book_detail"),
]