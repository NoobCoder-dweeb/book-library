from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.db import connection
from app.models import Book

class Command(BaseCommand):
    help = "Truncate all tables in the database"
    
    def handle(self, *args, **options) -> None:
        books = Book.objects.all()
        if not books:
            self.stdout.write(self.style.ERROR("No books to truncate."))
            return

        books.delete()
        self.stdout.write(self.style.SUCCESS("All books truncated successfully."))