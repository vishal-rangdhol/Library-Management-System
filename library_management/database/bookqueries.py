import sqlite3
from library_management.database.db_connection import DbConnection

class BookQueries:

    def __init__(self, db_file):
        self.db = DbConnection(db_file)
        self.connection = self.db.connect()
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE NOT NULL,
            copies_available INTEGER NOT NULL
        );
        """
        self.cursor.execute(query)
        self.connection.commit()

    # ---------------------------------------
    # ISBN GENERATION LOGIC
    # ---------------------------------------
    def generate_isbn(self, book_id, title):
        prefix = "BK"
        short = title[:2].upper()
        index = f"{book_id:03d}"  # 3-digit numbering
        return f"{prefix}{short}{index}"

    # ---------------------------------------
    # ADD BOOK (AUTO ISBN)
    # ---------------------------------------
    def add_book(self, title, author, copies_available):
        try:
            # Step 1: Insert temporary ISBN to satisfy NOT NULL
            temp_isbn = "TEMP"

            query = """INSERT INTO books (title, author, isbn, copies_available)
                       VALUES (?, ?, ?, ?)"""
            self.cursor.execute(query, (title, author, temp_isbn, copies_available))
            self.connection.commit()

            # Last inserted row
            book_id = self.cursor.lastrowid

            # Step 2: Generate ISBN
            isbn = self.generate_isbn(book_id, title)

            # Step 3: Update final ISBN
            update_query = """UPDATE books SET isbn = ? WHERE id = ?"""
            self.cursor.execute(update_query, (isbn, book_id))
            self.connection.commit()

            print(f"\n✔ Book added! Generated ISBN = {isbn}")
            return book_id, isbn

        except sqlite3.IntegrityError:
            raise Exception("Book already exists with this ISBN")
        except sqlite3.Error as e:
            raise Exception(f"Database Error: {e}")

    # ---------------------------------------
    def get_book_by_isbn(self, isbn):
        query = "SELECT * FROM books WHERE isbn = ?"
        self.cursor.execute(query, (isbn,))
        return self.cursor.fetchone()

    def get_all_books(self):
        query = "SELECT * FROM books"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_book_by_id(self, book_id):
        query = "SELECT * FROM books WHERE id = ?"
        self.cursor.execute(query, (book_id,))
        return self.cursor.fetchone()

    def update_quantity(self, book_id, qty):
        query = "UPDATE books SET copies_available = ? WHERE id = ?"
        self.cursor.execute(query, (qty, book_id))
        self.connection.commit()

    def remove_book(self, book_id):
        query = "DELETE FROM books WHERE id = ?"
        self.cursor.execute(query, (book_id,))
        self.connection.commit()

    def close_connection(self):
        self.db.close()







# import sqlite3
# from library_management.database.db_connection import DbConnection

# class BookQueries:

#     def __init__(self, db_file):
#         self.db_file = db_file
#         self.db = DbConnection(self.db_file)
#         self.connection = self.db.connect()
#         self.cursor = self.connection.cursor()
#         self.create_table()


#     def create_table(self):
#         create_table_query = """
#         create table if not exists books(
#         id integer primary key autoincrement,
#         title text not null,
#         author text not null,
#         isbn text  unique not null,
#         copies_available integer not null
#         )"""

#         self.cursor.execute(create_table_query)
#         self.connection.commit()
#         # print('Books table created successfully')


#     def add_book(self, title, author, isbn, copies_available):
#         try:
#             add_book_query = """insert into books (title, author, isbn, copies_available) values(?, ?, ?, ?)"""

#             self.cursor.execute(add_book_query,(title, author, isbn, copies_available))
#             self.connection.commit()
#             book_id = self.cursor.lastrowid
#             print(f"Book with id:[{book_id}] added successfully")
#             return book_id
        
#         except sqlite3.Error as e:
#             print(f'Database Error: {e}')


#     def get_book(self, book_id):
#         try:
#             get_book_query = """select * from books where book_id= ?;"""
#             self.cursor.execute(get_book_query,(book_id,))
#             book = self.cursor.fetchone()
#             self.connection.commit()
#             print(book)
#             return book

#         except sqlite3.Error as e:
#             print(f'Database Error: {e}')



#     def get_all_books(self):
#         try:
#             get_all_book_query = """select * from books;"""
#             self.cursor.execute(get_all_book_query)
#             book = self.cursor.fetchall()
#             self.connection.commit()
#             print(book)
#             return book

#         except sqlite3.Error as e:
#             print(f'Database Error: {e}')


#     def remove_book(self, book_id):
#         try:
#             book_to_be_removed = """delete from books where id = ?;"""
#             self.cursor.execute(book_to_be_removed,(book_id,))
#             self.connection.commit()
#             print(f'Book with ID: {book_id} removed successfully!!!')

#         except sqlite3.Error as e:
#             print(f'Database Error: {e}')   


#     def update_book(self, book_id, title = None, author = None, isbn = None, copies_available= None):
#         update_fields = []
#         values = []

#         if not update_fields:
#             print(f'Column U Provided Does Not Exist. \n Please Provide A Valid One...')

#         if title:
#             update_fields.append('title = ?')
#             values.append(title)

#         if author:
#             update_fields.append('author = ?')
#             values.append(author)

#         if isbn:
#             update_fields.append('isbn = ?')
#             values.append(isbn)

#         if copies_available:
#             update_fields.append('copies_available = ?')
#             values.append(copies_available)

#         if not update_fields:
#             print('Please Provide Any Column Field To Update')
#             return
        
#         update_query = f"update books set {(';' .join(update_fields))} where id = ?;"
#         values.append(book_id)
        
#         try:
#             self.cursor.execute(update_query, tuple(values))
#             self.connection.commit()
#             print('Book Updated Successfully!!')
        
#         except sqlite3.Error as e:
#             print(f"Database Error: {e}")


  



#     def close_connection(self):
#         self.db.close()


# # book = BookQueries("library.db")
# # book.add_book('power of subconscious mind','cillian murphy','POSMCM', 100 )
# # book.add_book('Eat that frog','luther king','ETFLK', 50 )
# # book.add_book('Bhagwat Gita', 'Shri Krishna', 'BGSK', 1000)
# # book.add_book('Dopamine Detox', 'Thibbaut Meurisse','DDTM' ,1000)

# # book.get_book(3)
# # book.get_all_books()

# # book.remove_book(2)
# # book.update_book(4, author='Brian Tracy')

# # book.close_connection()