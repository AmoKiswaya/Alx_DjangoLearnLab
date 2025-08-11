from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from .models import Book
from .serializers import BookSerializer


class ListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class DetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class CreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        current_year = timezone.now().year
        if serializer.validated_data['publication_year'] > current_year:
            raise ValidationError({"publication_year": "publication year cannot be in the future"})
        serializer.save() 

class UpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        current_year = timezone.now().year
        if serializer.validated_data['publication_year'] > current_year:
            raise ValidationError({"publication_year": "publication year cannot be in the future"})
        serializer.save() 


class DeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated] 
