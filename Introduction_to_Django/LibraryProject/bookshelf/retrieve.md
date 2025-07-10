# Call retrieve function object.all() using a for loop to show details of the Book instance.

## Import Book class from model.py file in bookshelf app.
>>> from bookkshelf.models import Book

## Use for loop to get details of the Book instance.
>>> for i in Book.objects.all():
        print(i.id, i.title, i.author, i.publication_year)

## Shell output
2 1984 George Orwell 1949        