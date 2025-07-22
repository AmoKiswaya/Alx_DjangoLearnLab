import os
import sys 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings") 

import django
django.setup()

from .models import Author, Book, Library, Librarian 

def query_books_by_author(author_name):
    """Query all books by a specific author."""
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"Books by {author_name}:")
        for book in books:
            print(f"  - {book.title}")
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return None

def list_books_in_library(library_name):
    """List all books in a library."""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library_name}:")
        for book in books:
            print(f"  - {book.title} by {book.author.name}")
        return books
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None

def retrieve_librarian_for_library(library_name):
    """Retrieve the librarian for a library."""
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        print(f"Librarian for {library_name}: {librarian.name}")
        return librarian
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None
    except Librarian.DoesNotExist:
        print(f"No librarian found for library '{library_name}'.")
        return None

# Example usage and testing
if __name__ == "__main__":
    print("=== Django Relationship App Query Samples ===\n")
    
    # Sample data creation 
    
    # Create sample authors
    author1 = Author.objects.create(name="George Orwell")
    
    # Create sample books
    book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1)
   
    # Create sample library
    library = Library.objects.create(name="Nairobi National Library")
    library.books.add(book1)
    
    # Create sample librarian
    librarian = Librarian.objects.create(name="Amos Kiswaya", library=library)
    
    
    # Example queries
    print("1. Query all books by a specific author:")
    query_books_by_author("George Orwell")
    print()
    
    print("2. List all books in a library:")
    list_books_in_library("Nairobi National Library") 
    print()
    
    print("3. Retrieve the librarian for a library:")
    retrieve_librarian_for_library("Nairobi National Library")
    print()
    
    # Alternative query methods using Django ORM
    print("=== Alternative Query Methods ===\n")
    
    # Query books by author using author ID
    print("Books by author (using author object):")
    try:
        author = Author.objects.get(name="George Orwell")
        books = author.book_set.all()  # Using reverse foreign key
        for book in books:
            print(f"  - {book.title}")
    except Author.DoesNotExist:
        print("Author not found")
    print()
    
    # Query library through librarian
    print("Library through librarian:")
    try:
        librarian = Librarian.objects.get(name="Amos Kiswaya")
        library = librarian.library
        print(f"  - {librarian.name} works at {library.name}")
    except Librarian.DoesNotExist:
        print("Librarian not found")
    print()
    
    # Query using select_related for better performance
    print("Books with authors (optimized query):")
    books = Book.objects.select_related('author').all()
    for book in books:
        print(f"  - {book.title} by {book.author.name}")