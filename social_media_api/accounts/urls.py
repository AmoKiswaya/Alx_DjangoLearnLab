from django.urls import path, include
from .views import UserRegistrationView, UserLoginView, UserProfileView, UserViewSet
from django.conf.urls.static import static
from django.conf import settings 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet) 

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('', include(router.urls)), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 