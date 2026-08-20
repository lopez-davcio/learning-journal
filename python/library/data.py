from pathlib import Path
import json

"""
A  module serving as a database to save all the information from execution to execution
"""


"""
A dictionary of all the books that the library owns in which keys are isbn and values are book attributes
"""
inventory = dict()


"""
A dict of dicts to store the utils's users, key = user_number, value = user object
"""
users = dict()


def load_inventory_users():
    global inventory, users
    from book import Book
    from user import User
    inventory = load_data('inventory_database.json', Book)
    users = load_data('user_database.json', User)


def load_data(file_address, cls):
    try:
        path = Path(file_address)
        contents = path.read_text()
    except FileNotFoundError:
        print('A file seems to be missing')
    else:
        content_json = json.loads(contents)
        objects_dict = from_dict(cls, content_json)
        return objects_dict
    

def from_dict(cls, data):    
    return {key:cls(**value) for key, value in data.items()}


def save_inventory_users():
    save_data('inventory_database.json', book_to_dict())
    save_data('user_database.json', user_to_dict())


def save_data(file_address, serializable_dict):
    """Converts the object into a dictionary and save it in json format"""
    
    try:
        path = Path(file_address)
        content_json = json.dumps(serializable_dict)
        path.write_text(content_json)
    except FileNotFoundError:
        print('It seems there is a missing file')


def book_to_dict():
    return {
        key:{
            'isbn':value._isbn,
            'title':value._title,
            'author':value._author, 
            'current_user':value._current_user,        
            'past_users':value._past_users,
            }
        for key, value in inventory.items()
    }

        
def user_to_dict():
    return {
        key:{       
            "user_number":value._user_number,
            "user_name":value._user_name,
            "current_books":value._current_books,  
            "past_books":value._past_books,
            }                   
        for key, value in users.items()
    }
        




    