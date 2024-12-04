from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.User_login,name='login' ),
    path('student/<slug:slug>',views.student_page,name='student_page' ),
    path('Register',views.register,name='students_registration'),
    path('log_out',views.log_out,name='log_out'),
#     path('student/<slug:slug>/Search-Books',views.st_books,name='st_search_books' ),
#     path('Student/Search-Book-By-<str:str>',views.search_books,name='st_search_books_by'),
#     path('Student/List-All-Books',views.list_all_books,name='st_list_all_books')

    
    
 ]
