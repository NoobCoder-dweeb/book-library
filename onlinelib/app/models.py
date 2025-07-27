from django.db import models

# Create your models here.
class Book(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    year = models.IntegerField(null=True, blank=True)
    publisher = models.CharField(max_length=100, blank=True, null=True)
    image_url_s = models.URLField(blank=True, null=True)
    image_url_m = models.URLField(blank=True, null=True)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.title} by {self.author}"