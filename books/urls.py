from django.contrib import admin
from django.urls import path,re_path
from . import views

urlpatterns = [

    path('BookComplete/', views.Bookcomplete.as_view(), name='BookComplete'),

 ]

