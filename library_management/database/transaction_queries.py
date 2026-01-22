import sqlite3
from library_management.database.db_connection import DbConnection

class TransactionQueries:

    def __init__(self, db_file):
        self.db = DbConnection(db_file)
        self.connection = self.db.connect()
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            book_id INTEGER NOT NULL,
            borrowed_date TEXT NOT NULL,
            returned_date TEXT NULL,
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY(book_id) REFERENCES books(id) ON DELETE CASCADE
        );
        """
        self.cursor.execute(query)
        self.connection.commit()

    def borrow_book(self, user_id, book_id, borrowed_date):
        try:
            query = """INSERT INTO transactions (user_id, book_id, borrowed_date)
                       VALUES (?, ?, ?);"""
            self.cursor.execute(query, (user_id, book_id, borrowed_date))
            self.connection.commit()

            transaction_id = self.cursor.lastrowid

            # Reduce copies
            update_query = """UPDATE books
                              SET copies_available = copies_available - 1
                              WHERE id = ?"""
            self.cursor.execute(update_query, (book_id,))
            self.connection.commit()

            return transaction_id

        except sqlite3.Error as e:
            raise Exception(f"Database Error (borrow): {e}")

    def return_book(self, transaction_id, returned_date):
        try:
            t = self.get_transaction_by_id(transaction_id)
            if not t:
                raise Exception("Transaction not found")

            book_id = t[2]

            update_trans = """UPDATE transactions
                              SET returned_date = ?
                              WHERE id = ?"""
            self.cursor.execute(update_trans, (returned_date, transaction_id))
            self.connection.commit()

            update_book = """UPDATE books
                             SET copies_available = copies_available + 1
                             WHERE id = ?"""
            self.cursor.execute(update_book, (book_id,))
            self.connection.commit()

            return book_id

        except sqlite3.Error as e:
            raise Exception(f"Database Error (return): {e}")

    def get_transaction_by_id(self, transaction_id):
        query = "SELECT * FROM transactions WHERE id = ?"
        self.cursor.execute(query, (transaction_id,))
        return self.cursor.fetchone()

    def get_transactions_by_user(self, user_id):
        query = "SELECT * FROM transactions WHERE user_id = ?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def close_connection(self):
        self.db.close()




# import sqlite3
# from library_management.database.db_connection import DbConnection

# class TransactionQueries:

#     def __init__(self, db_file):
#         self.db_file = db_file
#         self.db = DbConnection(self.db_file)
#         self.connection = self.db.connect()
#         self.cursor = self.connection.cursor()
#         self.create_table()

#     def create_table(self):
#         create_table_query= """
#         create table if not exists transactions(
#         id integer primary key autoincrement,
#         user_id text not null,
#         book_id  integer not null,
#         borrowed_date  text not null,
#         returned_date text null,
#         foreign key (user_id) references users (user_id) on delete cascade
#         foreign key (book_id) references books(id) on delete cascade
#         );"""

#         self.cursor.execute(create_table_query)
#         self.connection.commit()
#         # print('\nTable Created Successfully!!!')


#     def borrow_book(self, user_id, book_id, borrowed_date):

#         try:
#             insert_query = """insert into transactions(user_id, book_id, borrowed_date) values(?, ?, ?);"""
#             self.cursor.execute(insert_query,(user_id, book_id, borrowed_date))
#             self.connection.commit()
#             transaction_id = self.cursor.lastrowid

#             update_query = """update books set copies_available = copies_available-1 where id = ?"""
#             self.cursor.execute(update_query,(book_id,))
#             self.connection.commit()
#             print(f'Book ID: {book_id}\nBorrowed by: {user_id}\n Transaction ID: {transaction_id}')
#             return transaction_id
#         except sqlite3.Error as e:
#             print(f'Database Error: {e}')


#     def get_transaction_by_id(self, transaction_id):
#         select_query = """select * from transactions where id = ?"""
#         self.cursor.execute(select_query,(transaction_id,))
#         transaction = self.cursor.fetchone()
#         print(transaction)
#         return transaction
    
#     def get_transaction_by_user_id(self, user_id):
#         select_query = """select * from transactions where user_id = ?"""
#         self.cursor.execute(select_query,(user_id,))
#         transactions = self.cursor.fetchall()
#         print(transactions)
#         return transactions


#     def return_book(self, transaction_id, returned_date):
#         try:
#             transaction = self.get_transaction_by_id(transaction_id)
#             book_id = transaction[2]

#             return_query = """update transactions set returned_date = ? where id = ?"""

#             self.cursor.execute(return_query, (returned_date, transaction_id))
#             self.connection.commit()
            
#             update_query = """update books set copies_available = copies_available +1 where id = ?"""
#             self.cursor.execute(update_query, (book_id,))
#             self.connection.commit()
            
#             print(f'Book ID: {book_id}\nReturned On:{returned_date}')
#             return book_id, returned_date
        
#         except sqlite3.Error as e:
#             print(f'Database Error: {e}')


#     def close_connection(self):
#         self.db.close()

# # transaction_queries = TransactionQueries('library.db')
# # transaction_queries.borrow_book('STVI04', 3, '2025-03-22')
# # transaction_queries.borrow_book('STSA02', 1, '2025-03-22')
# # transaction_queries.get_transaction_by_id(1)
# # transaction_queries.return_book(1,'2025-03-24')
# # transaction_queries.get_transaction_by_user_id('STSA02')


# # transaction_queries.close_connection()