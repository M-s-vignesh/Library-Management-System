from django.contrib import admin
from django.urls import path,re_path
from . import views

urlpatterns = [
    path('Librarian/<slug:slug>/', views.librarian_page, name='librarian' ),
    path('Librarian/<slug:slug>/search-books', views.search, name='search_books' ),
    path('Login', views.librarian_login, name='librarian_login'),
    path('logout', views.log_out, name='log_out'),
    path('Librarian/<slug:slug>/Add-Books', views.add_books, name='add_books' ),
    path('Librarian/<slug:slug>/Add-Book-Codes', views.add_book_codes, name='add_book_codes' ),
    path('Librarian/<slug:slug>/List-All-Books', views.list_all_books, name='list_all_books'),
    path('Search-Book-By-<str:str>', views.search_books, name='search_books_by'),
    path('Loan-Book', views.loan_books, name='loan_books'),
    path('Return-Book', views.return_book, name='return_book'),
    path('return-book-autocomplete/', views.ReturnBookAutocomplete.as_view(), name='return-book-autocomplete'),
    path('studentid-autocomplete/', views.StudentIdAutocomplete.as_view(), name='studentid-autocomplete'),
    path('book-autocomplete/', views.BookAutocomplete.as_view(), name='book-autocomplete'),
    path('book-code-autocomplete/', views.BookCodeAutocomplete.as_view(), name='book-code-autocomplete'),
    path('student-id-autocomplete/', views.StudentIdAutocomplete.as_view(), name='student-id-autocomplete'),
    path('book-title-autocomplete/', views.BookTitleAutocomplete.as_view(), name='book-title-autocomplete'),
    path('List-Students/',views.list_students,name = 'list_students'),
    path('Librarian-Delete-Book/', views.delete_books, name = 'delete_books'),
    path('Librarian/Profile', views.profile, name = 'librarian_profile'),
    path('Librarian/<slug:slug>/Update-Profile', views.Update, name = 'update_profile'),
    path('Librarian/<slug:slug>/Reset-Password', views.reset_password, name = 'reset_password'),

 ]

