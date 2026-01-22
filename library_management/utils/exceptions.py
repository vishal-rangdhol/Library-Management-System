class LibraryError(Exception):
    pass

class UserAlreadyExists(LibraryError):
    def __init__(self, message = "User Already Exists...!!!"):
        self.message = message
        super().__init__(message)

class UserNotFound(LibraryError):
    def __init__(self, message = "User Not Found...!!!"):
        self.message = message
        super().__init__(message)

class DuplicateBookISBNError(LibraryError):
    def __init__(self, message = "Book Already Exists...!!!"):
        self.message = message
        super().__init__(message)

class BookNotFound(LibraryError):
    def __init__(self, message = "Book Not Found...!!!"):
        self.message = message
        super().__init__(message)

class TransactionNotFound(LibraryError):
    def __init__(self, message = "Transaction Not Found...!!!"):
        self.message = message
        super().__init__(message)