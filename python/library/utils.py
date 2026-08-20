from book import Book
from user import User
import data


"""A module for the logic of the library's operations"""


          
def lend_book():
    """    
    Check that book is owned by the library and that the user is registered in the library. Then lends the book to the user, assigns the user as current_user in that book entry and the book as current_book in the user entry.    
    """
    book_isbn = Book.obtain_and_validate_isbn()
     
    if Book.is_book_in_inventory(book_isbn):        
        print('Please add the user number of the user whom you want to lend the book:')
        user_number = input()
        if User.is_user_registered(user_number):
            if data.inventory[book_isbn].current_user == 'library':
                data.inventory[book_isbn].current_user = user_number
                data.users[user_number].current_books = book_isbn
                print(f'The book {book_isbn} has been lent to the user {user_number}')
            else:
                print(f'Book {book_isbn} is not available.')
        else:
            print(f'The user number {user_number} is not registered in the library.')
    else:
        print(f"The library does not own the book with isbn: {book_isbn}.")
    
  

def return_book():
    """
    Returns the book to the library, checks if the system recognises that user as the original borrower, assigns library as current borrower,
    adds the user as past borrowers of the book, adds the book as past books borrowed by the user and deletes the book from current books of user.
    """
    print('Please add the isbn number of the book you want to return:')
    book_isbn = input()    
    if book_isbn in data.inventory.keys(): 
        print('Please add the user number of the user who is returning the book:')
        user_number = input()
        if data.inventory[book_isbn].current_user == user_number:
            data.inventory[book_isbn].current_user = 'library'
            data.inventory[book_isbn].past_users.append(user_number)
            data.users[user_number].past_books.append(book_isbn)
            print(f'The book {book_isbn} has been returned by the user {user_number}')
            try:
                data.users[user_number].current_books.remove(book_isbn)
            except:
                print('That isbn was not in the list of books borrowed by the user, please investigate further.')         

        else:
            print(f'The system does not recognize user {user_number} as the current borrower of book {book_isbn}.')
    else:
        print(f"The library does not own the book with isbn: {book_isbn}.")
    

def display_users():
    """Display the user number and name of all the users of the library"""
    for key, value in data.users.items():        
        print(f"User number: {value.user_number}, user name: {value.user_name}.")         


def display_inventory():
    """Display the isbn, the name and the current user of all books of the library"""
    for key, value in data.inventory.items():        
        print(f"Book isbn: {value.isbn}, book name: {value.title.title()}, current_user: {value.current_user}")
    

def display_available_books():
    """Display the isbn, the name and the current holder, library, of all books currently available of the library"""
    for key, value in data.inventory.items():
        if value.current_user == 'library':
            print(f"Book isbn: {value.isbn}, book name: {value.title.title()}, current_user: {value.current_user}")


def display_book_location():
    """Display the book isbn and its current holder"""
    print('Please add the book isbn:')
    book_isbn = input()
    
    if book_isbn in data.inventory.keys():
        print(f"The book with isbn: {book_isbn} is currently held by: {data.inventory[book_isbn].current_user}")
    else:
        print(f"The library does not own the book with isbn: {book_isbn}.")


def display_book_info():
    """Display all information of a book"""
    print("Please add book's isbn:")
    book_isbn = input()
    if book_isbn in data.inventory.keys():
        print(data.inventory[book_isbn])       
    else:
        print(f"The library does not own the book with isbn: {book_isbn}.")
    

def display_user_current_book():
    """Display books currently held by a user"""
    print('Please add the user number:')
    user_number = input()
    if user_number in data.users.keys():
        print(f'The user number {user_number} is currently holding books:')
        if data.users[user_number].current_books:
            for book in data.users[user_number].current_books:
                print(f'Isbn: {book}')
        else:
            print('None')
    else:
        print(f'The user number {user_number} is not registered in the library.')