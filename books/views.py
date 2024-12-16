from django.shortcuts import render
from .models import Books
from dal import autocomplete

# Create your views here.

class Bookcomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        qs = Books.objects.filter(coded_books__lt = 5)
        if self.q:
            qs = qs.filter(title__istartswith=self.q)
        return qs
