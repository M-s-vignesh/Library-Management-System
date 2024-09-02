from django.contrib import admin
from .models import Books,book_code
# Register your models here.

admin.site.register(Books)
admin.site.register(book_code)
