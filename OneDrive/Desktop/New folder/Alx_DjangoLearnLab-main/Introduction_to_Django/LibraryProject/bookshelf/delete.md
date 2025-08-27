from bookshelf.models import Book

Retrieve and delete the book
book = Book.objects.get(title="Nineteen Eighty-Four") book.delete()

Confirm deletion
Book.objects.all() # Expected output: <QuerySet []>
