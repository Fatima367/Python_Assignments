# Create a class Book with a class variable total_books. 
# Add a class method increment_book_count() to increase the 
# count when a new book is added.

class Book:
    total_books = 0

    @classmethod
    def increment_book_count(cls):
        cls.total_books += 1

    def __init__(self, book_title):
        self.book_title = book_title
        self.increment_book_count()

    @classmethod
    def display_total_books(cls):
        print(f"Total books added: {cls.total_books}")

book: Book = Book("Pride and Prejudice")
book2: Book = Book("Harry Potter and the Sorcerer's Stone")
book3: Book = Book("The Great Gatsby")

Book.display_total_books()