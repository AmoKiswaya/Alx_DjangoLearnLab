# bookshelf/urls.py
from django.urls import path
from . import views
from .views import book_list
from .views import create_book
from .views import edit_book
from .views import delete_book


urlpatterns = [
    path('', views.book_list, name='book_list'),  # <-- This is the URL name used in redirect
    path('create/', views.create_book, name='create_book'),
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
]
