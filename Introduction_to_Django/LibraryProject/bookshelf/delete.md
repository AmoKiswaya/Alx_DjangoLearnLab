# Use delete method to delete book instance.

## Import Book class from model.py file in bookshelf app.
>>> from bookkshelf.models import Book

## Retrieve the book first by title.
>>> book_1 = Book.objects.get(title="Nineteen Eighty-Four") 

## Delete book instance using the delete method.
>>> book_1.delete()
## Shell output
(1, {'bookshelf.Book': 1}) 