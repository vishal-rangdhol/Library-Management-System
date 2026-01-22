import sqlite3 
from sqlite3 import Error

class DbConnection:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_file)
            # print('Connection Formed successfully')
            self.connection.execute('PRAGMA FOREIGN_KEYS = ON')
            return self.connection
        
        except Error as e:
            print(f'DataBase Error: {e}')


    def close(self):
        self.connection.close()
        # print('Connection Closed !!!')

# db = DbConnection('library.db')
# db.connect()
# db.close()
    