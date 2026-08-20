import random
import data

class User:
    """A class to model the library users"""

    def __init__(self, user_number, user_name, current_books=[], past_books=[]):
        self._user_number = user_number
        self._user_name = user_name
        self._current_books = current_books
        self._past_books = past_books

    def __str__(self):
        return f'User number: {self.user_number}, user name: {self.user_name}, current books: {self.current_books}, past books: {self.past_books}.'

    @property
    def user_number(self):
        return self._user_number
    
    @property
    def user_name(self):
        return self._user_name

    @property
    def current_books(self):
        return self._current_books
        
    @current_books.setter
    def current_books(self, book):
        self._current_books.append(book)
    
    @property
    def past_books(self):
        return self._past_books
        
    @past_books.setter
    def past_books(self, book):
        self._past_books.append(book)

    @staticmethod
    def add_new_user():
        """Generate a random user, take the user name as input, and instantiate a user object"""
        user_number = User._generate_user_number()
        user_name = User._obtain_user_name()
        new_user = User(user_number, user_name)
        data.users[user_number] = new_user      
        print(f'User {user_name} has been added to the users register.')

    @staticmethod
    def _generate_user_number():
        """Generates a user number and checks that it's not being used"""
        while True:
            user_number = random.randint(100,999)
            user_number = str(user_number)
            if user_number in data.users.keys():
                continue
            else:
                break
        print(f'The assigned user number of the new user is {user_number}.') 
        return user_number
    
    @staticmethod
    def _obtain_user_name():
        """Asks input user name and checks it's not being used"""
        print('Please add the user name:')
        while True:
            user_name = input().upper()            
            if user_name in data.users.keys():
                print('That user name is not available, please choose a different user number:')
            else:
                return user_name
            
    @staticmethod
    def is_user_registered(user_number):
        return user_number in data.users.keys()            
            
