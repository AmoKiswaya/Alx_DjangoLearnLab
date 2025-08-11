from django.urls import path
from .views import ListView
from .views import DetailView
from .views import DeleteView
from .views import CreateView
from .views import UpdateView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('books/', ListView.as_view(), name='list-books'),
    path('books/<int:pk>/', DetailView.as_view(), name='book-detail'),
    path('books/create/', CreateView.as_view(), name='create-book'),
    path('books/update/', UpdateView.as_view(), name='update-book'),
    path('books/delete/', DeleteView.as_view(), name='delete-book'),
    path('api/auth/token/', obtain_auth_token, name='api_token_auth'),
]