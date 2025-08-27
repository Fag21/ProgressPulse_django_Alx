from relationship_app.models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
def books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    books = Book.objects.filter(author=author)
    print(f"Books by {author_name}:")
    for book in books:
        print(f"- {book.title}")

# 2. List all books in a library
def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    books = library.books.all()
    print(f"Books in the library {library_name}:")
    for book in books:
        print(f"- {book.title}")

# 3. Retrieve the librarian for a library
def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    librarian = Librarian.objects.get(library=library)
    print(f"The librarian for {library_name} is {librarian.name}")

# Test the queries
if __name__ == "__main__":
    # Query 1: Books by a specific author (change 'Author Name' to an existing author)
    books_by_author('Author Name')

    # Query 2: Books in a specific library (change 'Library Name' to an existing library)
    books_in_library('Library Name')

    # Query 3: Librarian for a specific library (change 'Library Name' to an existing library)
    librarian_for_library('Library Name')
    