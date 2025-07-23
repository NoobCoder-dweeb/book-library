from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True, null=True)
    price = models.FloatField(null=True, blank=True)
    isbn = models.CharField(max_length=13, primary_key=True)
    cover_image = models.URLField(blank=True, null=True)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.title} by {self.author}"