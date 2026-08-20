
1. **Project Overview** 
2. **Motivation** 
3. **Installation & Usage** 
4. **Design Decisions & Thought Process**
5. **Challenges & Solutions** 
6. **Key learnings** 
7. **Testing**
8. **Future Improvements** 


# Project Overview
This project simulates a basic command-line library management system. It allows users to interact with a virtual library by performing operations such as adding books, registering users, lending and returning books, and retrieving information about users or books.   
It emphasizes a modular and object-oriented approach, dividing logic between classes (Book, User), a utility module (utils) for core operations, and a data module that manages persistent storage using JSON files. This project serves both as a practical demonstration of OOP in Python and as a foundation for a more complex system in the future

# Motivation
After studying the module "Introduction to Python" at university, going through the book "Python crash course" by Eric Matthes, and learnt through several Udemy courses about Python and Git technology, I wanted to put in practice concepts like:
-   Object-oriented programming: classes, inheritance, and subclasses  
-   Modular code organization using files, modules, and imports  
-   Persistent storage with `pathlib` and `JSON` files  
-   Exception handling  
-   Loops and user interaction through input prompts
-   Git configuration and basic usage like branches, merging, commiting and pushing.


# Installation & Usage
#### To install and run the project:
-   Clone the repository 
-   Ensure the directory structure includes the following files:  
        `main.py` – main execution script  
        `book.py`, `user.py`, `utils.py`, `data.py`, `mock_data.py`  
        `inventory_database.json`, `user_database.json` (optional, can be created automatically)
-   (Optional) Load mock data:    
        To prefill the system with books, users, and transactions, run:  
        `python mock_data.py`
            
-   Run the program:  
        `python main.py`                
All user and book data is saved persistently across sessions in .json files.


# Design Decisions & Thought Process
## The initial layout consists of:

- Classes Book and User: Defined in their respective modules, these classes are responsible for creating instances of books and users. The created objects are then passed to the data module for storage.

- utils Module: Contains the core functionality and operations of the library, such as borrowing, returning, and managing books.

- data Module: Handles the persistence logic, saving and retrieving data from JSON files. These files act as a lightweight database.

- JSON Files: Two separate JSON files store books and users, respectively. The data is structured as dictionaries with keys being ISBN (for books) or user_number (for users), and values being dictionaries representing the object data.

- main Module: Serves as the entry point of the application.

There is a separate module called mock_data that can be run to populate the system with books, users, and transactions, simulating a typical library workflow.


# Challenges & Solutions
**Challenge:** Python objects cannot be directly stored in JSON format.  
**Solution:** 
There are two primary approaches to address this:

Object Serialization: Convert Python objects into dictionaries using methods like . __dict__ before saving to JSON, and deserialize them back into objects upon loading. This method is more elaborate and can introduce unnecessary complexity.  
Direct Dictionary Storage (Chosen Approach): Store data directly as dictionaries rather than objects. This approach is simpler and better aligned with the scope of the project.

# Key learnings
JSON and Python Objects: One of the main goals was to practice working with objects, modifying their attributes and persisting user input across sessions. However, JSON does not support direct serialization of Python class instances.
Initially, the intent was to save Book and User objects directly in JSON format. This proved unfeasible, leading to the decision to store the object data as dictionaries instead.
This experience reinforced the importance of understanding data serialization and the limitations of different storage formats.

 
In addition, this project provided solid practice in applying object-oriented programming principles:

-   Encapsulation was applied by defining attributes as protected (e.g., _isbn, _user_number) to prevent direct external modification.
-   Static methods were used for class-wide functionality not dependent on object instances, such as creating new users (User.add_new_user()) or   validating input (Book.obtain_and_validate_isbn()).
-   Using @property and setters created controlled access points to the attributes, ensuring better internal data consistency.
-   This structure emphasized clean separation of responsibilities and control over how data is accessed and modified, a cornerstone of good OOP practices.

# Testing
The best approach for testing this project, and the initial intention was, to use the pytest library. However, the resulting functions of this project might not be good candidates for that, they would probably need to be refactored to be testable.
Instead, I use a manual approach. Comprehensively testing all the possible scenarios.

# Future Improvements
More Functional Code: Several parts of the utils module could be broken down into smaller, more reusable functions.

Shorter utils Module: Right now, the utils.py file handles all major operations, but some of these (like display_user_current_book, return_book, etc.) could be logically moved into the Book or User class to improve cohesion and encapsulation.

Refactor for Testability: Functions relying on input() can be refactored to accept parameters instead, which would make them suitable for unit testing.
