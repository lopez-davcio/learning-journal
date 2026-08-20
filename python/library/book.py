import data

class Book:
    """ A class to model the book object, create new books"""

    def __init__(self, isbn, title, author, current_user='library', past_users=[]):
        self._isbn = isbn
        self._title = title
        self._author = author 
        self._current_user = current_user        
        self._past_users = past_users

    def __str__(self):
        return f'Isbn: {self._isbn}, title: {self._title}, author: {self._author}, current user: {self._current_user}, past users: {self._past_users}'

    @property
    def isbn(self):
        return self._isbn
    
    @property
    def title(self):
        return self._title
    
    @isbn.setter
    def isbn(self, isbn):
        self._isbn = isbn

    @property
    def current_user(self):
        return self._current_user
    
    @current_user.setter
    def current_user(self, current_user):
        self._current_user = current_user
    
    @property
    def past_users(self):
        return self._past_users  

    @past_users.setter
    def past_users(self, past_users):
        self._past_users = past_users     
    
    @staticmethod
    def add_new_book():
        """
        Obtain isbn, title and author, create object and store it in data.inventory
        """
        isbn = Book.obtain_and_validate_isbn()                
        print("Please add the book's title:")
        title = input()
        print("Please add the book's author:")
        author = input()
        new_book = Book(isbn, title, author)        
        data.inventory[isbn] = new_book
        print(f"Book {title} has been added to the library's inventory")

    @staticmethod
    def obtain_and_validate_isbn():
        """Ask to input isbn, validate it, must ba a 5 digit number, return isbn as str"""
        print('Please add a 5 digit isbn:')
        while True:
            isbn = input()
            if len(isbn) == 5:
                try:
                    isbn = int(isbn)
                    break
                except ValueError:
                    print('The isbn must be a 5 digit number, please try again:')
            else:
                print('The isbn must be a 5 digit number, please try again:')
                continue
        return str(isbn)

    @staticmethod
    def is_book_in_inventory(book_isbn):
        return book_isbn in data.inventory.keys()
