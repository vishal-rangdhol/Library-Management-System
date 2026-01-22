from library_management.services.user_services import UserServices
from library_management.services.book_services import BookServices
from library_management.services.transaction_services import TransactionServices
from library_management.utils.exceptions import *

DB_NAME = "library.db"
ADMIN_PASS = "libraryAdmin@123"


# -------------------------------------------------
# SAFE INPUT HELPERS
# -------------------------------------------------
def safe_int_input(prompt):
    value = input(prompt).strip()
    if not value.isdigit():
        raise ValueError("Input must be a number")
    return int(value)


# -------------------------------------------------
# INIT SERVICES
# -------------------------------------------------
def establish_connection():
    global users, books, transactions
    users = UserServices(DB_NAME)
    books = BookServices(DB_NAME)
    transactions = TransactionServices(DB_NAME)


# -------------------------------------------------
# USER REGISTRATION
# -------------------------------------------------
def register_user():
    name = input("Enter student name: ").strip()
    email = input("Enter student email: ").strip()

    try:
        user_id = users.register_student(name, email)
        print("\n✔ User Registered Successfully")
        print(f"Student Name : {name}")
        print(f"User ID      : {user_id}\n")
    except UserAlreadyExists:
        print("❌ User already exists")


# -------------------------------------------------
# LIBRARIAN MENU
# -------------------------------------------------
def librarian_menu():
    pwd = input("Enter librarian password: ").strip()
    if pwd != ADMIN_PASS:
        print("❌ Access denied!")
        return

    while True:
        print("\n--- LIBRARIAN MENU ---")
        print("1. Add Book")
        print("2. Delete Book")
        print("3. Update Quantity")
        print("4. Back")

        ch = input("Enter choice: ").strip()

        # ADD BOOK (AUTO ISBN)
        if ch == "1":
            try:
                title = input("Title  : ").strip()
                author = input("Author : ").strip()
                qty = safe_int_input("Quantity: ")

                book_id, isbn = books.add_book(title, author, qty)

                print("\n✔ Book Added Successfully")
                print(f"Internal Book ID : {book_id}")
                print(f"Generated ISBN   : {isbn}\n")

            except ValueError:
                print("❌ Quantity must be a number")
            except Exception as e:
                print(f"❌ {e}")

        # DELETE BOOK
        elif ch == "2":
            try:
                bid = safe_int_input("Enter Book ID (number): ")
                books.remove_book(bid)
                print("✔ Book removed")
            except ValueError:
                print("❌ Invalid Book ID (numbers only)")
            except Exception as e:
                print(f"❌ {e}")

        # UPDATE QUANTITY
        elif ch == "3":
            try:
                bid = safe_int_input("Book ID (number): ")
                qty = safe_int_input("New Quantity: ")
                books.update_book_quantity(bid, qty)
                print("✔ Quantity updated")
            except ValueError:
                print("❌ Invalid input (numbers only)")
            except Exception as e:
                print(f"❌ {e}")

        elif ch == "4":
            return
        else:
            print("❌ Invalid choice")


# -------------------------------------------------
# BORROW BOOK
# -------------------------------------------------
def borrow_book():
    user_id = input("Enter user ID: ").strip().upper()
    isbn = input("Enter book ISBN: ").strip().upper()

    try:
        book = books.get_book_by_isbn(isbn)
        book_id = book[0]  # internal ID
        tid = transactions.issue_book(user_id, book_id)
        print(f"✔ Book Issued Successfully | Transaction ID: {tid}")
    except BookNotFound:
        print("❌ No book found with this ISBN")
    except Exception as e:
        print(f"❌ {e}")


# -------------------------------------------------
# RETURN BOOK
# -------------------------------------------------
def return_book():
    try:
        tid = safe_int_input("Enter Transaction ID (number): ")
        transactions.return_book(tid)
        print("✔ Book Returned Successfully")
    except ValueError:
        print("❌ Transaction ID must be a number")
    except Exception as e:
        print(f"❌ {e}")


# -------------------------------------------------
# VIEW BOOKS
# -------------------------------------------------
def view_all_books():
    books_list = books.get_all_books()
    print("\n--- ALL BOOKS ---")
    if not books_list:
        print("No books available")
    for b in books_list:
        print(b)


# -------------------------------------------------
# VIEW TRANSACTION BY ID
# -------------------------------------------------
def view_transaction_by_id():
    try:
        tid = safe_int_input("Enter Transaction ID (number): ")
        print(transactions.get_transaction_by_id(tid))
    except ValueError:
        print("❌ Transaction ID must be a number")
    except Exception:
        print("❌ Transaction not found")


# -------------------------------------------------
# VIEW TRANSACTIONS BY USER
# -------------------------------------------------
def view_transaction_by_user():
    uid = input("Enter User ID: ").strip().upper()
    records = transactions.get_transactions_by_user(uid)
    if not records:
        print("No transactions found")
    else:
        for r in records:
            print(r)


# -------------------------------------------------
# MAIN LOOP
# -------------------------------------------------
def main():
    establish_connection()

    while True:
        print("\n=== LIBRARY MANAGEMENT SYSTEM ===")
        print("1. Register User")
        print("2. Manage Book (Librarian Only)")
        print("3. Borrow Book (Student Only)")
        print("4. Return Book")
        print("5. View All Books")
        print("6. View Transaction by ID")
        print("7. View Transaction by User ID")
        print("8. Exit")

        ch = input("Enter choice: ").strip()

        if ch == "1":
            register_user()
        elif ch == "2":
            librarian_menu()
        elif ch == "3":
            borrow_book()
        elif ch == "4":
            return_book()
        elif ch == "5":
            view_all_books()
        elif ch == "6":
            view_transaction_by_id()
        elif ch == "7":
            view_transaction_by_user()
        elif ch == "8":
            print("Goodbye 👋")
            break
        else:
            print("❌ Invalid choice")








# from library_management.services.user_services import UserServices
# from library_management.utils import exceptions
# from library_management.services.book_services import BookServices
# from library_management.services.transaction_services import TransactionServices

# # It can be used while registering the librarian
# ADMIN_PASS = 'libraryAdmin@123'

# # Database file name
# DB_NAME = 'library.db'

# def establish_connection():
#     global user_services, book_services, transaction_services
#     user_services = UserServices(DB_NAME)
#     book_services = BookServices(DB_NAME)
#     transaction_services = TransactionServices(DB_NAME)

# def break_connection():
#     user_services.close_connection()
#     book_services.close_connection()
#     transaction_services.close_connection()

# def main_menu():
#     print("1. Register User")
#     print("2. Manage Book (Librarian Only)")
#     print("3. Borrow Book (Student Only)")
#     print("4. Return Book")
#     print("5. View All Book")
#     print("6. View Transaction Details By ID")
#     print("7. View Transaction Details By User ID")
#     print("8. Exit")
#     choice = input("\nPlease Select An Option: ")
#     return choice


# def user_registration():
#     print('\n1. Librarian (Only Admin)')
#     print('2. Student')
#     user_type =input("Choose user type: ")
#     try:
#         if user_type == '1':
#             admin_pass = input('Enter Admin Password:')
#             if admin_pass == ADMIN_PASS:
#                 name = input("Enter Name: ").title()
#                 email = input("Enter email: ").lower()
#                 user_id = user_services.register_librarian(name=name, email=email)
#                 print(f'\nLibrarian Name: {name}')
#                 print(f'Registered ID: {user_id}')
#                 print(f'Registration Successful!')

#             else:
#                 print("\nIncorrect password Please Try Again!")

#         elif user_type == '2':
#             name = input("Enter Name: ").title()
#             email = input("Enter email: ").lower()
#             user_id = user_services.register_student(name=name, email=email)
#             print(f'\Student Name: {name}')
#             print(f'Registered ID: {user_id}')
#             print(f'Registration Successful!')
            
#         else:
#             print("Invalid Choice")
    
#     except exceptions.UserAlreadyExists as e:
#         print(f'Error: {e}')

# def manage_book():
#     librarian_id = input("Enter your Librarian user ID: ").upper()
#     try:
#         if user_services.is_admin(user_id=librarian_id):
#             print('1. Add Book')
#             print('2. Update Book')
#             print('3. Remove Book')
#             choice = input("Enter your choice: ")
#             if choice =='1':
#                 title = input("Enter book title: ")
#                 author = input("Enter author: ")
#                 isbn = input("Enter isbn: ")
#                 copies_available = input("Enter copies_available: ")
#                 try:
#                     book = book_services.add_book(title=title,
#                                                   author=author,
#                                                   isbn=isbn,
#                                                   copies_available=int(copies_available))
#                     print(f'Added Book: {title}')
#                     print(f'Generated Book ID: {book[0]}')
#                 except ValueError as e:
#                     print(f'Error: {e}')
#                 except exceptions.DuplicateBookISBNError as e:
#                     print(f'Error: {e}')




#                     # missing code
#             elif choice == '2':
#                 book_id = input("Enter book ID:")
#                 try:
#                     book = input('Enter book title()')





                    
                


















# def main():
#     print("*---*Welcome To The Library*---*")
#     print("\nConnection Established\n")
#     establish_connection()

#     while True:
#         choice = main_menu()
#         if choice == '1':
#             print()
        
#         elif choice == '8':
#             print('Connection Closed')
#             break_connection()
#             print("Thank You, Visit Again!!")
#             break
        












# # user_service = UserServices('library.db')
# # print("Connection Successfully !!!")

# # try:
# #    print('ID:', user_service.register_librarian('Shahid', 'Shahid@gmail.co'))
# #    print('ID:', user_service.register_librarian('Sagar', 'sagar@gmail.com'))

# # except exceptions.UserAlreadyExists as e:
# #     print(f'Error: {e}')

# # try:
# #    #  print('ID:', user_service.register_student('Vishal', 'Vishal@gmail.co'))
# #     print('ID:', user_service.register_student('Manohar', 'mano@gmail.com'))

# # except exceptions.UserAlreadyExists as e:
# #     print(f'Error: {e}')
# # user_service.close_connection()




# # try:
# #     print('ID:', user_service.register_librarian('Reyleigh', 'darkking@gmail.com'))

# # except exceptions.UserAlreadyExists as e:
# #     print(f'Error: {e}')

# # user_service.close_connection()




# # try:
# #     print('User Data', user_service.get_user('LBRE07'))

# # except exceptions.UserAlreadyExists as e:
# #     print(f'Error: {e}')

# # user_service.close_connection()



# # try:
# #     print("Is Student ID:", user_service.is_student('STVI01'))

# # except exceptions.UserNotFound as e:
# #     print(f'Error: {e}')
# # user_service.close_connection()


# # try:
# #     print("Is Librarian ID:", user_service.is_admin('LBRE07'))

# # except exceptions.UserNotFound as e:
# #     print(f'Error: {e}')
# # user_service.close_connection()


# # book_services = BookServices('library.db')
# # try:
# #     print(book_services.get_all_books())
# # except exceptions.BookNotFound as e:
# #     print(f'Error: {e}')
# # book_services.close_connection()


# # book_services = BookServices('library.db')
# # try:
# #     print(book_services.add_book('Rich Dad & Poor Dad', 'Rober Kiyosaki & Sharon Lechter', 1235869475, 1))

# # except exceptions.DuplicateBookISBNError as e:
# #     print(f'Error: {e}')
# # book_services.close_connection()

