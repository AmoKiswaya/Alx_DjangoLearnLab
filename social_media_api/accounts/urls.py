from django.urls import path, include
from .views import UserRegistrationView, UserLoginView, UserProfileView, FollowUserView, UnfollowUserView
from django.conf.urls.static import static
from django.conf import settings 
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 