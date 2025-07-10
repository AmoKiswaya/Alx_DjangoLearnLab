# Use delete method to delete book instance.

## Import Book class from model.py file in bookshelf app.
>>> from bookshelf.models import Book

## Retrieve the book first by title.
>>> book = Book.objects.get(title="Nineteen Eighty-Four") 

## Delete book instance using the delete method.
>>> book.delete()
## Shell output
(1, {'bookshelf.Book': 1}) 