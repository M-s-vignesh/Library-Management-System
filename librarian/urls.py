from django.contrib import admin
from django.urls import path,re_path
from . import views

urlpatterns = [
    path('Librarian/<slug:slug>/',views.librarian_page,name='librarian' ),
    path('Librarian/<slug:slug>/search-books',views.search,name='search_books' ),
    path('Login',views.librarian_login,name='librarian_login'),
    path('Librarian/<slug:slug>/Add-Books',views.add_books,name='add_books' ),
    path('Librarian/<slug:slug>/Add-Book-Codes',views.add_book_codes,name='add_book_codes' ),
    path('List-All-Books',views.list_all_books,name='list_all_books'),
    path('Search-Book-By-<str:str>',views.search_books,name='search_books_by'),
    path('Loan-Book',views.loan_books,name='loan_books'),
    path('load_codes/',views.loadcodes,name ='load_codes'),
    path('Return-Book',views.return_book,name='return_book'),
    path('book-title-autocomplete/',views.BookTitleAutocomplete.as_view(),name='book-title-autocomplete'),
    path('studentid-autocomplete/',views.StudentIdAutocomplete.as_view(),name='studentid-autocomplete'),
    
]

