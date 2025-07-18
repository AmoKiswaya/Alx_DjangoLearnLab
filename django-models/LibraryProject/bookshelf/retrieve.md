# Use the .get method to get the instance of book created.

## Import Book class from model.py file in bookshelf app.
>>> from bookkshelf.models import Book

## Use .get method to get book instance.
>>> book = Book.objects.get(title=1984) 

## Use print statement to get attribute values of the book instance.
>>> print("ID", book.id) 
## Shell output
ID: 2
>>> print("Title:", book.title) 
## Shell output
Title: 1984
>>> print("Author:", book.author)
## Shell output
Author: George Orwell
>>> print("Publication Year:", book.publication_year)
## Shell output
Publication Year: 1949