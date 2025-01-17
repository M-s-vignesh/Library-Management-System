from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.User_login,name='login' ),
    path('student/<slug:slug>',views.student_page,name='student_page' ),
    path('Register',views.register,name='students_registration'),
    path('log_out',views.log_out,name='log_out'),
    path('student/<slug:slug>/Search-Books',views.st_books,name='st_search_books' ),
    path('student/<slug:slug>/Search-Book-By-<str:str>',views.search_books,name='st_search_books_by'),
    path('student/<slug:slug>/List-All-Books',views.list_all_books,name='st_list_all_books'),
    path('student/<slug:slug>/Loaned-Books',views.loaned_books,name='st_loaned_books'),
    path('student/<slug:slug>/Profile',views.student_profile,name='student_profile'),
    path('student/<slug:slug>/Update-Student-Profile',views.update_student_profile,name='update_student_profile'),
    path('student/<slug:slug>/Reset-Password', views.reset_password, name = 'student_reset_password'),
 ]
