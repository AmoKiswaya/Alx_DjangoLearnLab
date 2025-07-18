# Use python sql create operation to create a Book instance.

## Import Book class from model.py file in bookshelf app.

>>> from bookshelf.models import Book

>>> Book = Book.objects.create(
        title = "1984",
        author = "George Orwell",
        publication_year = 1949
)

## Call objects.all method on the Book instance to see output of book created.

>>> from bookshelf.models import Book
>>> Book.objects.all() 

## Shell output.
<QuerSet [<Book: Book object (2)>]> 