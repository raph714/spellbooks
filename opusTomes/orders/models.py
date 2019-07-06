from django.db import models
from books.models import Book, DNDPage

class Order(models.Model):
    books = models.ManyToManyField(Book, related_name="orders")
    dnd_pages = models.ManyToManyField(DNDPage, related_name="orders")

    address = models.CharField(max_length=200)
    apartment_number = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)

    sent = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    tracking_number = models.CharField(max_length=200)
