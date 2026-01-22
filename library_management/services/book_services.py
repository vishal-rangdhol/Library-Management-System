from library_management.database.bookqueries import BookQueries
from library_management.utils.exceptions import BookNotFound

class BookServices:
    def __init__(self, db_file):
        self.book_queries = BookQueries(db_file)

    def add_book(self, title, author, qty):
        return self.book_queries.add_book(title, author, qty)

    def get_book_by_isbn(self, isbn):
        book = self.book_queries.get_book_by_isbn(isbn)
        if not book:
            raise BookNotFound
        return book

    def get_all_books(self):
        return self.book_queries.get_all_books()

    def update_book_quantity(self, book_id, qty):
        self.book_queries.update_quantity(book_id, qty)

    def remove_book(self, book_id):
        self.book_queries.remove_book(book_id)

    def close_connection(self):
        self.book_queries.close_connection()





# from library_management.models.books import Books
# from library_management.database.bookqueries import BookQueries
# from library_management.utils import exceptions

# class BookServices:
#     def __init__(self, db_file):
#         self.db_file = db_file
#         self.book_queries = BookQueries(self.db_file)

#     def get_one_book(self, book_id):
#         book = self.book_queries.get_book(book_id=book_id)
#         if book:
#             return book
#         else:
#             raise exceptions.BookNotFound
        

#     def get_all_books(self):
#         return self.book_queries.get_all_books()
    

#     def add_book(self, title, author, isbn, copies_available):
#         book = Books(title=title,
#                     author=author, 
#                     isbn=isbn, 
#                     copies_available=copies_available)
        
#         book_id = self.book_queries.add_book(title=title, 
#                                              author=author, 
#                                              isbn=isbn, 
#                                              copies_available=copies_available)
        
#         if book_id:
#             return self.get_one_book(book_id=book_id)
#             # return book_id
#         else:
#             raise exceptions.DuplicateBookISBNError
        

#     def update_book(self, book_id, title=None, author=None, isbn=None, copies_available=None):
#         book_id = self.book_queries.update_book( book_id, title=title, author=author, isbn=isbn, copies_available=copies_available)

#         if book_id:
#             return self.get_one_book(book_id=book_id)
        

#     def remove_book(self, book_id):
#         book = self.get_one_book(book_id=book_id)
#         book_id = self.book_queries.remove_book(book_id=book[0])
#         return book_id
    

#     def is_available(self, book_id):
#         book = self.get_one_book(book_id=book_id)
#         return book[4] > 0
    

#     def close_connection(self):
#         self.book_queries.close_connection()