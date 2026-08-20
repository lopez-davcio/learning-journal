from book import Book
from user import User
import utils
import data

"""
Simulate a database loading books and users from module data
"""

menu_print = """
Select an option:
1.  Add new book
2.  Add new user
3.  Lend book
4.  Return book
5.  Display all library users
6.  Display full inventory
7.  Display available books
8.  Display book location
9.  Display book info
10. Display user's current book
Q. Quit
"""

"""
Load inventory_database and user_database at program initiation
"""
data.load_inventory_users()

while True:    
    print(menu_print)
    choice = input()
    if choice == '1':
        print('You chose: Add new book.')
        Book.add_new_book()
    elif choice == '2':
        print('You chose: Add new user.')
        User.add_new_user()    
    elif choice == '3':
        print('You chose: Lend book.')
        utils.lend_book()
    elif choice == '4':
        print('You chose: Return book.')
        utils.return_book()
    if choice == '5':
        print('You chose: Display all library users.')
        utils.display_users()
    elif choice == '6':
        print('You chose: Display full inventory.')
        utils.display_inventory()    
    elif choice == '7':
        print('You chose: Display available books.')
        utils.display_available_books()
    elif choice == '8':
        print('You chose: Display book location.')
        utils.display_book_location()
    elif choice == '9':
        print('You chose: Display book info.')
        utils.display_book_info()    
    elif choice == '10':
        print("You chose: Display user's current book.")
        utils.display_user_current_book()        
    elif choice.lower() == 'q':
        data.save_inventory_users()
        break
    print("\nPress 'q' to quit or any key to continue:")
    choice = input().lower()
    if choice == 'q':
        data.save_inventory_users()
        break
    else:
        continue
    
    


