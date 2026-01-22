from library_management.models.users import Librarian, Student
from library_management.database.user_queries import UserQueries
from library_management.utils.exceptions import UserAlreadyExists, UserNotFound

class UserServices:
    def __init__(self, db_file):
        self.user_queries = UserQueries(db_file)

    def register_student(self, name, email):
        user_id = self.user_queries.add_user(name, email, "student")
        if not user_id:
            raise UserAlreadyExists
        return user_id

    def register_librarian(self, name, email):
        user_id = self.user_queries.add_user(name, email, "librarian")
        if not user_id:
            raise UserAlreadyExists
        return user_id

    def get_user(self, user_id):
        user = self.user_queries.get_user_by_id(user_id)
        if user:
            return user
        raise UserNotFound

    def close_connection(self):
        self.user_queries.close_connection()








# from library_management.models.users import Librarian, Student
# from library_management.database.user_queries import UserQueries
# from library_management.utils.exceptions import UserAlreadyExists, UserNotFound

# class UserServices:
#     def __init__(self, db_file):
#         self.db_file = db_file
#         self.user_queries = UserQueries(self.db_file)


#     def register_librarian(self, name, email):
#         librarian = Librarian(name=name, email=email)
#         librarian_id = self.user_queries.add_user(username=librarian.name,
#                                                   email=librarian.email,
#                                                   role=librarian.role)
        
#         if librarian_id:
#             return librarian_id
        
#         else:
#             raise UserAlreadyExists
        


#     def register_student(self, name, email):
#         student = Student(name=name, email=email)
#         student_id = self.user_queries.add_user (username=student.name,
#                                                  email=student.email,
#                                                  role=student.role)
#         if student_id:
#             print(f'student has registered successfully!!!\n***Details Given Below***\nStudent Name: {name}\nStudent ID: {student_id}')
#             return student_id

#         else:
#             raise UserAlreadyExists
        


#     def get_user(self, user_id):
#         user = self.user_queries.get_user_by_id(user_id=user_id)

#         if user:
#             return user
        
#         else:
#             raise UserNotFound
        


#     def is_student(self, user_id):
#         user = self.user_queries.get_user_by_id(user_id)

#         if not user:
#             print(f'Entered userid {user_id} does not belongs to any student')
#             raise UserNotFound
        
#         # return self.get_user(user_id=user_id)[3] == 'student'               -----alternative----

#         elif user[3] == 'student':
#             print(f'Entered userid {user_id} belongs to a student')
#             return True
        
#         # return self.get_user(user_id=user_id)[3] == 'librarian'            -----alternative-----
        
#     # is_student and is_admin both are same methods. Here, tried different approaches


#     def is_admin(self, user_id):
#         user = self.user_queries.get_user_by_id(user_id)
#         if user:
#             if user[3] == 'librarian':
#                 print(True)
#                 return True

#         else:
#             print(False)
#             return False  
        
        
#     def close_connection(self):
#         self.user_queries.close_connection()
