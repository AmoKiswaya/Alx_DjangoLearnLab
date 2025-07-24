# Update book title attribute to Nineteen Eighty-Four using the filter and update method.

## Import Book class from model.py file in bookshelf app.
>>> from bookkshelf.models import Book

## Use filter and update method to update the title.
>>> Book.objects.filter(title="1984").update(title="Nineteen Eighty-Four) 

## Import Book class from model.py file in bookshelf app.
>>> from bookkshelf.models import Book

## Use print statement to show updated title.
>>> book = Book.objects.get(title="Nineteen Eighty-Four")
>>> print(book.title)

## Shell output
Nineteen Eighty-Four
