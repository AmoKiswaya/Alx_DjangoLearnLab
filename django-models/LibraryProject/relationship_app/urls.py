from django.urls import path
from . import views
from .views import list_books 
from .views import LibraryDetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from .views import admin_view
from .views import librarian_view
from .views import member_view


urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
]
