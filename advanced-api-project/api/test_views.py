
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient 
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.utils import timezone
from .models import Book, Author
import json


class BookAPITestCase(TestCase):
    """
    Comprehensive test suite for Book API endpoints
    """
    
    def setUp(self):
        """Set up test data and authentication"""
        self.client = APIClient()
        
        # Create test users
        self.authenticated_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        self.another_user = User.objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='anotherpassword123'
        )
        
        # Create authentication tokens
        self.token = Token.objects.create(user=self.authenticated_user)
        self.another_token = Token.objects.create(user=self.another_user)
        
        # Create test authors
        self.author1 = Author.objects.create(name='Author One')
        self.author2 = Author.objects.create(name='Author Two')
        self.author3 = Author.objects.create(name='Search Author')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Test Book 1',
            author=self.author1,
            publication_year=2020
        )
        
        self.book2 = Book.objects.create(
            title='Another Book',
            author=self.author2,
            publication_year=2021
        )
        
        self.book3 = Book.objects.create(
            title='Search Test Book',
            author=self.author1,
            publication_year=2019
        )
        
        # Test data for creating new books
        self.valid_book_data = {
            'title': 'New Test Book',
            'author': self.author1.id,
            'publication_year': 2022
        }
        
        self.invalid_book_data_future_year = {
            'title': 'Future Book',
            'author': self.author1.id,
            'publication_year': timezone.now().year + 1
        }
        
        self.invalid_book_data_missing_fields = {
            'title': 'Incomplete Book'
        }
        
        self.invalid_book_data_nonexistent_author = {
            'title': 'Book with Invalid Author',
            'author': 999,
            'publication_year': 2022
        }

    def authenticate_user(self, user_token=None):
        """Helper method to authenticate user"""
        token = user_token or self.token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    
    def clear_authentication(self):
        """Helper method to clear authentication"""
        self.client.credentials()


class BookListViewTests(BookAPITestCase):
    """Test cases for ListView (GET /api/books/)"""
    
    def test_list_books_unauthenticated(self):
        """Test that unauthenticated users can view book list"""
        url = reverse('list-books')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
    
    def test_list_books_authenticated(self):
        """Test that authenticated users can view book list"""
        self.authenticate_user()
        url = reverse('list-books')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
    
    def test_filter_books_by_title(self):
        """Test filtering books by title"""
        url = reverse('list-books')
        response = self.client.get(url, {'title': 'Test Book 1'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Book 1')
    
    def test_filter_books_by_author_id(self):
        """Test filtering books by author ID"""
        url = reverse('list-books')
        response = self.client.get(url, {'author': self.author1.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        # Both books should be by author1
        for book in response.data['results']:
            self.assertEqual(book['author'], self.author1.id)
    
    def test_filter_books_by_publication_year(self):
        """Test filtering books by publication year"""
        url = reverse('list-books')
        response = self.client.get(url, {'publication_year': '2020'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['publication_year'], 2020)
    
    def test_search_books_by_title(self):
        """Test searching books by title"""
        url = reverse('list-books')
        response = self.client.get(url, {'search': 'Another'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Another Book')
    
    def test_search_books_by_author_name(self):
        """Test searching books by author name"""
        url = reverse('list-books')
        response = self.client.get(url, {'search': 'Author Two'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['author'], self.author2.id)
    
    def test_ordering_books_by_title(self):
        """Test ordering books by title"""
        url = reverse('list-books')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles))
    
    def test_ordering_books_by_publication_year_desc(self):
        """Test ordering books by publication year descending"""
        url = reverse('list-books')
        response = self.client.get(url, {'ordering': '-publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years, reverse=True))


class BookDetailViewTests(BookAPITestCase):
    """Test cases for DetailView (GET /api/books/<id>/)"""
    
    def test_get_book_detail_unauthenticated(self):
        """Test that unauthenticated users can view book details"""
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['author'], self.book1.author.id)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
    
    def test_get_book_detail_authenticated(self):
        """Test that authenticated users can view book details"""
        self.authenticate_user()
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['author'], self.book1.author.id)
    
    def test_get_nonexistent_book_detail(self):
        """Test getting details for a non-existent book"""
        url = reverse('book-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookCreateViewTests(BookAPITestCase):
    """Test cases for CreateView (POST /api/books/create/)"""
    
    def test_create_book_authenticated_valid_data(self):
        """Test creating a book with valid data while authenticated"""
        self.authenticate_user()
        url = reverse('create-book')
        response = self.client.post(url, self.valid_book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(response.data['title'], self.valid_book_data['title'])
        self.assertEqual(response.data['author'], self.valid_book_data['author'])
        self.assertEqual(response.data['publication_year'], self.valid_book_data['publication_year'])
        
        # Verify the book was actually created in the database
        created_book = Book.objects.get(id=response.data['id'])
        self.assertEqual(created_book.title, self.valid_book_data['title'])
        self.assertEqual(created_book.author.id, self.valid_book_data['author'])
    
    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books"""
        self.clear_authentication()
        url = reverse('create-book')
        response = self.client.post(url, self.valid_book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 3)
    
    def test_create_book_future_publication_year(self):
        """Test creating a book with future publication year (should fail)"""
        self.authenticate_user()
        url = reverse('create-book')
        response = self.client.post(url, self.invalid_book_data_future_year, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
        self.assertEqual(Book.objects.count(), 3)
    
    def test_create_book_missing_required_fields(self):
        """Test creating a book with missing required fields"""
        self.authenticate_user()
        url = reverse('create-book')
        response = self.client.post(url, self.invalid_book_data_missing_fields, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Book.objects.count(), 3)
    
    def test_create_book_nonexistent_author(self):
        """Test creating a book with non-existent author"""
        self.authenticate_user()
        url = reverse('create-book')
        response = self.client.post(url, self.invalid_book_data_nonexistent_author, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Book.objects.count(), 3)
    
    def test_create_book_current_year(self):
        """Test creating a book with current year (should succeed)"""
        self.authenticate_user()
        current_year_data = {
            'title': 'Current Year Book',
            'author': self.author1.id,
            'publication_year': timezone.now().year
        }
        url = reverse('create-book')
        response = self.client.post(url, current_year_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
    
    def test_create_book_with_new_author(self):
        """Test creating a book with a different existing author"""
        self.authenticate_user()
        book_data = {
            'title': 'Book by Author Two',
            'author': self.author2.id,
            'publication_year': 2022
        }
        url = reverse('create-book')
        response = self.client.post(url, book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_book = Book.objects.get(id=response.data['id'])
        self.assertEqual(created_book.author, self.author2)


class BookUpdateViewTests(BookAPITestCase):
    """Test cases for UpdateView (PUT/PATCH /api/books/update/<id>/)"""
    
    def test_update_book_authenticated_valid_data(self):
        """Test updating a book with valid data while authenticated"""
        self.authenticate_user()
        updated_data = {
            'title': 'Updated Book Title',
            'author': self.author2.id,
            'publication_year': 2021
        }
        url = reverse('update-book', kwargs={'pk': self.book1.id})
        response = self.client.put(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, updated_data['title'])
        self.assertEqual(self.book1.author.id, updated_data['author'])
        self.assertEqual(self.book1.publication_year, updated_data['publication_year'])
    
    def test_partial_update_book_authenticated(self):
        """Test partially updating a book while authenticated"""
        self.authenticate_user()
        partial_data = {'title': 'Partially Updated Title'}
        url = reverse('update-book', kwargs={'pk': self.book1.id})
        response = self.client.patch(url, partial_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, partial_data['title'])
        # Other fields should remain unchanged
        self.assertEqual(self.book1.author, self.author1)
        self.assertEqual(self.book1.publication_year, 2020)
    
    def test_partial_update_author_only(self):
        """Test updating only the author of a book"""
        self.authenticate_user()
        partial_data = {'author': self.author2.id}
        url = reverse('update-book', kwargs={'pk': self.book1.id})
        response = self.client.patch(url, partial_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.author, self.author2)
        # Other fields should remain unchanged
        self.assertEqual(self.book1.title, 'Test Book 1')
        self.assertEqual(self.book1.publication_year, 2020)
    
    def test_update_book_unauthenticated(self):
        """Test that unauthenticated users cannot update books"""
        self.clear_authentication()
        updated_data = {'title': 'Should Not Update'}
        url = reverse('update-book', kwargs={'pk': self.book1.id})
        response = self.client.put(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Test Book 1')  # Should remain unchanged
    
    def test_update_book_future_publication_year(self):
        """Test updating a book with future publication year (should fail)"""
        self.authenticate_user()
        future_year_data = {
            'title': 'Future Book',
            'author': self.author1.id,
            'publication_year': timezone.now().year + 1
        }
        url = reverse('update-book', kwargs={'pk': self.book1.id})
        response = self.client.put(url, future_year_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.publication_year, 2020)  # Should remain unchanged
    
    def test_update_book_nonexistent_author(self):
        """Test updating a book with non-existent author"""
        self.authenticate_user()
        invalid_data = {
            'title': 'Updated Title',
            'author': 999,
            'publication_year': 2022
        }
        url = reverse('update-book', kwargs={'pk': self.book1.id})
        response = self.client.put(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.author, self.author1)  # Should remain unchanged
    
    def test_update_nonexistent_book(self):
        """Test updating a non-existent book"""
        self.authenticate_user()
        url = reverse('update-book', kwargs={'pk': 999})
        response = self.client.put(url, self.valid_book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookDeleteViewTests(BookAPITestCase):
    """Test cases for DeleteView (DELETE /api/books/delete/<id>/)"""
    
    def test_delete_book_authenticated(self):
        """Test deleting a book while authenticated"""
        self.authenticate_user()
        book_id = self.book1.id
        url = reverse('delete-book', kwargs={'pk': book_id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)
        self.assertFalse(Book.objects.filter(id=book_id).exists())
    
    def test_delete_book_unauthenticated(self):
        """Test that unauthenticated users cannot delete books"""
        self.clear_authentication()
        url = reverse('delete-book', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())
    
    def test_delete_nonexistent_book(self):
        """Test deleting a non-existent book"""
        self.authenticate_user()
        url = reverse('delete-book', kwargs={'pk': 999})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Book.objects.count(), 3)
    
    def test_delete_book_cascade_author_relationship(self):
        """Test that deleting a book doesn't delete the author (CASCADE behavior)"""
        self.authenticate_user()
        author_id = self.book1.author.id
        url = reverse('delete-book', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Author should still exist
        self.assertTrue(Author.objects.filter(id=author_id).exists())


class AuthenticationTests(BookAPITestCase):
    """Test cases for authentication and token functionality"""
    
    def test_obtain_auth_token(self):
        """Test obtaining authentication token"""
        url = reverse('api_token_auth')
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['token'], self.token.key)
    
    def test_obtain_auth_token_invalid_credentials(self):
        """Test obtaining token with invalid credentials"""
        url = reverse('api_token_auth')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)
    
    def test_token_authentication_works(self):
        """Test that token authentication works for protected endpoints"""
        self.authenticate_user()
        url = reverse('create-book')
        response = self.client.post(url, self.valid_book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_invalid_token_authentication(self):
        """Test authentication with invalid token"""
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid_token_here')
        url = reverse('create-book')
        response = self.client.post(url, self.valid_book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PermissionTests(BookAPITestCase):
    """Test cases for permission enforcement"""
    
    def test_read_only_permissions_unauthenticated(self):
        """Test that unauthenticated users have read-only access"""
        # Can read list
        url = reverse('list-books')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Can read detail
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Cannot create
        url = reverse('create-book')
        response = self.client.post(url, self.valid_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Cannot update
        url = reverse('update-book', kwargs={'pk': self.book1.id})
        response = self.client.put(url, self.valid_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Cannot delete
        url = reverse('delete-book', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_full_permissions_authenticated(self):
        """Test that authenticated users have full CRUD access"""
        self.authenticate_user()
        
        # Can create
        url = reverse('create-book')
        response = self.client.post(url, self.valid_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_book_id = response.data['id']
        
        # Can update
        url = reverse('update-book', kwargs={'pk': created_book_id})
        updated_data = {'title': 'Updated Title'}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Can delete
        url = reverse('delete-book', kwargs={'pk': created_book_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class EdgeCaseTests(BookAPITestCase):
    """Test cases for edge cases and error handling"""
    
    def test_empty_search_query(self):
        """Test search with empty query"""
        url = reverse('list-books')
        response = self.client.get(url, {'search': ''})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
    
    def test_invalid_filter_values(self):
        """Test filtering with invalid values"""
        url = reverse('list-books')
        response = self.client.get(url, {'publication_year': 'invalid_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return all books when filter is invalid
        self.assertEqual(len(response.data['results']), 3)
    
    def test_filter_by_nonexistent_author(self):
        """Test filtering by non-existent author ID"""
        url = reverse('list-books')
        response = self.client.get(url, {'author': 999})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
    
    def test_multiple_filters_combined(self):
        """Test combining multiple filters"""
        url = reverse('list-books')
        response = self.client.get(url, {
            'author': self.author1.id,
            'publication_year': '2020'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Book 1')
    
    def test_search_and_filter_combined(self):
        """Test combining search and filters"""
        url = reverse('list-books')
        response = self.client.get(url, {
            'search': 'Test',
            'author': self.author1.id
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return books that match both search and filter criteria
        self.assertGreaterEqual(len(response.data['results']), 1)
    
    def test_search_author_name_functionality(self):
        """Test searching by author name works correctly"""
        url = reverse('list-books')
        response = self.client.get(url, {'search': 'Search Author'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should find books by the author named 'Search Author'
        # Note: This test assumes your serializer includes author name in search
        # If not, you may need to adjust your search_fields in the view


class AuthorRelationshipTests(BookAPITestCase):
    """Test cases specific to Author-Book relationship"""
    
    def test_create_multiple_books_same_author(self):
        """Test creating multiple books by the same author"""
        self.authenticate_user()
        
        book_data_1 = {
            'title': 'First Book by Author',
            'author': self.author3.id,
            'publication_year': 2020
        }
        
        book_data_2 = {
            'title': 'Second Book by Same Author',
            'author': self.author3.id,
            'publication_year': 2021
        }
        
        url = reverse('create-book')
        
        # Create first book
        response1 = self.client.post(url, book_data_1, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Create second book by same author
        response2 = self.client.post(url, book_data_2, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        
        # Verify both books are by the same author
        book1 = Book.objects.get(id=response1.data['id'])
        book2 = Book.objects.get(id=response2.data['id'])
        self.assertEqual(book1.author, book2.author)
        self.assertEqual(book1.author, self.author3)
    
    def test_author_foreign_key_constraint(self):
        """Test that author foreign key constraint is enforced"""
        self.authenticate_user()
        
        # Try to create a book with a non-existent author ID
        invalid_data = {
            'title': 'Book with Invalid Author',
            'author': 999,
            'publication_year': 2022
        }
        
        url = reverse('create-book')
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Verify the book was not created
        self.assertFalse(Book.objects.filter(title='Book with Invalid Author').exists())
    
    def test_filter_books_by_multiple_authors(self):
        """Test filtering to get books by specific authors"""
        # Create additional books
        additional_book = Book.objects.create(
            title='Additional Book',
            author=self.author2,
            publication_year=2022
        )
        
        # Filter by author1
        url = reverse('list-books')
        response = self.client.get(url, {'author': self.author1.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # book1 and book3
        
        # Filter by author2
        response = self.client.get(url, {'author': self.author2.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # book2 and additional_book