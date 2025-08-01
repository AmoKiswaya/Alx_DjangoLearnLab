from django.urls import path
from django.urls import include
from .views import BookList
from .views import BookViewSet
from rest_framework.routers import DefaultRouter 
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all') 

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),  
     path('', include(router.urls)),
     path('auth/token/', obtain_auth_token, name='api-token-auth'),
]


