from django.contrib import admin

from .models import Book, DNDPage, SRDPage

admin.site.register(Book)
admin.site.register(DNDPage)
admin.site.register(SRDPage)
