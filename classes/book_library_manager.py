from sqlalchemy import false


class Book:
    """Represents a single book in the library."""
    
    def __init__(self, title: str, author: str, isbn: str, year: int):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.is_checked_out = False
    
    def __str__(self):
        status = "Checked Out" if self.is_checked_out else "Available"
        return f"'{self.title}' by {self.author} ({self.year}) - {status}"


class Library:
    """Manages a collection of books."""

    def __init__(self, name: str):
        self.name = name
        self.books = []  # List to store Book objects

    def add_book(self, book: Book) -> str:

        if self.find_book_by_isbn(book.isbn) :
            print(f"warning the book {book.title} is already in catalog")
            return False


        self.books.append(book)
        print( f" '{book.title}' by {book.author} added")
        return True


        #pass


    def find_book_by_isbn(self, isbn: str) -> Book | None:

        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def checkout_book(self, isbn: str) -> bool:
        """Checks out a book by ISBN if it's available."""
        book = self.find_book_by_isbn(isbn)

        # Guard Clause 1: Handle the case where the book doesn't exist.
        if not book:
            print(f"Error: Book with ISBN {isbn} not found.")
            return False

        # Guard Clause 2: Handle the case where the book is already checked out.
        if book.is_checked_out:
            print(f"Error: '{book.title}' is already checked out.")
            return False

        # --- Success Path ---
        # If we've gotten this far, the book exists and is available.
        book.is_checked_out = True
        print(f"Successfully checked out '{book.title}'.")
        return True







        """
        
        TODO: Implement this method
        Check out a book by ISBN if it's available.

        Args:
            isbn: The ISBN of the book to check out

        Returns:
            True if successful, False if book not found or already checked out
        """


    def return_book(self, isbn: str) -> bool:

        book=self.find_book_by_isbn(isbn)

        if not book:
            print(f"Error: Book with ISBN {isbn} not found.")
            return False

        if not book.is_checked_out:
            print(f"Error: '{book.title}' is not checked out.")
            return False



        book.is_checked_out = False
        print (f"succesSfully returned '{book.title}'.")
        return True





        """
        TODO: Implement this method
        Return a book by ISBN.

        Args:
            isbn: The ISBN of the book to return

        Returns:
            True if successful, False if book not found or wasn't checked out
        """
        pass

    def list_available_books(self) -> list[Book]:
        """Gets a list of all available (not checked out) books."""
        return [book for book in self.books if not book.is_checked_out]

        """
        TODO: Implement this method
        Get a list of all available (not checked out) books.

        Returns:
            List of Book objects that are available
        """
        pass

    def get_books_by_author(self, author: str) -> list[Book]:
        return [book for book in self.books if book.author == author]


        for author in  self.author:
            if author is author:
                lista_aut=[]
                lista_aut.append(self.title)
                print ()


        """
        TODO: Implement this method
        Find all books by a specific author.

        Args:
            author: The author name to search for

        Returns:
            List of Book objects by that author
        """
        pass



# Test your implementation
if __name__ == "__main__":
    # Create a library
    lib = Library("City Library")
    
    # Add some books
    book1 = Book("The Python Tutorial", "Guido van Rossum", "123-456", 1991)
    book2 = Book("Clean Code", "Robert Martin", "789-012", 2008)
    book3 = Book("The Pragmatic Programmer", "Hunt & Thomas", "345-678", 1999)
    book4 = Book("Python Tricks", "Dan Bader", "901-234", 2017)
    
    lib.add_book(book1)
    lib.add_book(book2)
    lib.add_book(book3)
    lib.add_book(book4)
    
    # Test finding a book
    print("Finding book by ISBN '789-012':")
    found = lib.find_book_by_isbn("789-012")
    print(f"  {found}\n")
   # bookie=
    print (book1)
    
    # Test checking out a book
    print("Checking out 'Clean Code':")
    success = lib.checkout_book("789-012")
    print(f"  Success: {success}")
    print(f"  {lib.find_book_by_isbn('789-012')}\n")

    # Test returning a book
    print("Returning 'Clean Code':")
    success = lib.return_book("789-012")
    print(f"  Success: {success}")
    print(f"  {lib.find_book_by_isbn('789-012')}\n")

    # Test listing available books
    print("Available books:")
    for book in lib.list_available_books():
        print(f"  {book}")
    print()
    
    # Test finding books by author
    print("Books by authors containing 'van Rossum':")
    for book in lib.get_books_by_author("Guido van Rossum"):
        print(f"  {book}")
    print()
    
