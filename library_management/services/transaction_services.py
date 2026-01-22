from datetime import datetime
from library_management.database.transaction_queries import TransactionQueries
from library_management.utils.exceptions import TransactionNotFound

class TransactionServices:
    def __init__(self, db_file):
        self.transaction_queries = TransactionQueries(db_file)

    def issue_book(self, user_id, book_id):
        borrowed_date = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        return self.transaction_queries.borrow_book(user_id, book_id, borrowed_date)

    def return_book(self, transaction_id):
        returned_date = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        return self.transaction_queries.return_book(transaction_id, returned_date)

    def get_transaction_by_id(self, tid):
        t = self.transaction_queries.get_transaction_by_id(tid)
        if not t:
            raise TransactionNotFound
        return t

    def get_transactions_by_user(self, user_id):
        return self.transaction_queries.get_transactions_by_user(user_id)

    def close_connection(self):
        self.transaction_queries.close_connection()





# from library_management.models.transactions import Transactions
# from library_management.database.transaction_queries import TransactionQueries
# from library_management.utils import exceptions
# from datetime import datetime

# class TransactionServices:
#     def __init__(self, db_file):
#         self.db_file = db_file
#         self.transaction_queries = TransactionQueries(self.db_file)

#     def get_transaction_by_id(self, transaction_id):
#         transaction = self.transaction_queries.get_transaction_by_id(transaction_id=transaction_id)
#         if transaction:
#             return transaction
#         else:
#             raise exceptions.TransactionNotFound
        
#     def get_transaction_by_user_id(self, user_id):
#         transactions = self.transaction_queries.get_transaction_by_user_id(user_id=user_id)
#         if transactions:
#             return transactions
        

#     def issue_book(self, user_id, book_id):
#         borrowed_transaction = Transactions(user_id=user_id,
#                                             book_id=book_id,
#                                             borrowed_date=datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"))
        
#         transaction_id = self.transaction_queries.borrow_book(user_id=borrowed_transaction.user_id,
#                                                               book_id=borrowed_transaction.book_id,
#                                                               borrowed_date=borrowed_transaction.borrowed_date)
#         if transaction_id:
#             return transaction_id
        

#     def return_book(self, transaction_id):
#         returned_transaction = self.transaction_queries.return_book(transaction_id=transaction_id,
#                                                                      returned_date=datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"))
#         if returned_transaction:
#             return returned_transaction
        

#     def is_returned(self, transaction_id):
#         transaction = self.get_transaction_by_id(transaction_id=transaction_id)
#         if transaction[4]:
#             return True
        

#     def close_connection(self):
#         self.transaction_queries.close_connection()