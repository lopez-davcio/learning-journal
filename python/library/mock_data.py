from book import Book
from user import User 
import data
import utils

"""
Code to run only to populate the system with books, users, and transactions, simulating a typical library workflow.
It stores a books catalog and a user list, instantiate book and user objects and save them into dictionaries data.inventory and data.users. It also generates mock transactions
"""

books_catalog = [
    ['handbook', 'ou', '40182'],
    ['notebook', 'ax', '58703'],
    ['manual', 're', '73219'],
    ['guide', 'lm', '46874'],
    ['journal', 'tz', '91562'],
    ['ledger', 'vk', '64301'],
    ['report', 'dn', '52987'],
    ['catalog', 'sm', '38429'],
    ['logbook', 'cy', '77740'],
    ['register', 'xp', '82016'],
    ['bulletin', 'fa', '31055'],
    ['record', 'uj', '69834'],
    ['paper', 'bo', '45972'],
    ['folio', 'xz', '87319'],
    ['briefing', 'ni', '59160'],
    ['summary', 'qe', '74528'],
    ['memo', 'kh', '62493'],
    ['transcript', 'ld', '35210'],
    ['outline', 'gw', '89974'],
    ['synopsis', 'zb', '47086']
]


library_users = [
    ['401', 'DLM'],
    ['587', 'QRT'],
    ['732', 'LNV'],
    ['468', 'BXP'],
    ['915', 'ZKC'],
    ['643', 'MAJ'],
    ['529', 'WUT'],
    ['397', 'CKY'],
    ['777', 'HGD'],
    ['820', 'NRQ'],
    ['310', 'JFL'],
    ['698', 'TVS'],
    ['459', 'UEM'],
    ['873', 'XZD'],
    ['591', 'RBA'],
    ['261', 'KON'],
    ['624', 'YMI'],
    ['352', 'GEH'],
    ['899', 'VDL'],
    ['470', 'SQC']
]


def load_books():
    for book in books_catalog:
        title = book[0]
        author = book[1]
        isbn = book[2]
        new_book = Book(isbn, title, author)
        data.inventory[isbn] = new_book
load_books()        

def load_users():
    for user in library_users:
        number = user[0]
        name = user[1]
        new_user = User(number, name)
        data.users[number] = new_user
load_users()


def mock_lend_transaction(book_isbn, user_number):
    if Book.is_book_in_inventory(book_isbn):        
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


def mock_return_transaction(book_isbn, user_number):       
    if book_isbn in data.inventory.keys():         
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

def load_mock_transactions():
    mock_lend_transaction('52987', '261')
    mock_lend_transaction('40182', '401')
    mock_lend_transaction('40182', '397')
    mock_lend_transaction('87319', '401')
    mock_return_transaction('87319', '401')
    mock_return_transaction('40182', '401')
    mock_lend_transaction('87319', '397')
    mock_lend_transaction('40182', '261')
    mock_return_transaction('52987', '261')
    mock_return_transaction('40182', '261')
    mock_lend_transaction('52987', '401')

load_mock_transactions()

data.save_inventory_users()