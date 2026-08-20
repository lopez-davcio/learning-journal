1. **Project Overview** 
2. **Motivation** 
3. **Installation & Usage** 
4. **Design Decisions & Thought Process**
5. **Challenges & Solutions** 
6. **Key learnings** 
7. **Future Improvements** 



# Project Overview

This project simulates a basic command-line university management system. It allows three different types of users (students, professors, and admins) to interact with the system in different ways:

* **Students** can view courses, enrol or deregister, check their credits, and view grades and GPA.
* **Professors** can view assigned courses and assign grades to students.
* **Admins** can manage accounts and courses (add, remove, archive).

The system is designed with multiple Python modules, each handling different parts of the logic (user types, enrolments, courses, etc.). It emphasizes an object-oriented and modular approach.

# Motivation

After finishing my previous project (a library system), I wanted to build something more complex that required more files, more classes, and more interactions between them.

For this project I specifically wanted to practice:

* Object-oriented programming in a slightly larger project, with inheritance between `User`, `Student`, `Professor`, and `Admin`.
* Building a more elaborate modular structure without running into circular imports or dependency issues.
* Applying **best practices** I’ve been learning, such as:
  * Using **private attributes and methods** (`_attribute`, `__method`) to better protect class internals.
  * Practicing **encapsulation**, so that each class is responsible for its own state and behaviour.
  * Respecting **separation of concerns**, making sure each module and class has a clear, single responsibility.
  * Writing code with maintainability in mind, avoiding giant utils files.
  * Maintaining clear and informative docstrings for functions and methods to improve code readability and understanding.


# Installation & Usage

#### To install and run the project:

* Clone the repository.
* Make sure the following files are present:
  `main.py`, `orchestrator.py`, `user.py`, `student.py`, `professor.py`, `admin.py`, `course.py`, `enrolment.py`, `grades.py`, `utils.py`, `data.py`.
* The program automatically runs `data.py` on startup to preload some mock users and courses.
* For demonstration, one **student**, one **professor**, and one **admin** account are created and their IDs are printed at launch.

  * If you want to log in with one of these accounts, use the printed ID.
  * The password for all preloaded accounts is an empty string.
* Start the program with:

  ```python
  main.py
  ```
* From there, you can either create a new account or log in with one of the preloaded accounts. Different menus will appear depending on whether you’re a student, professor, or admin.


# Design Decisions & Thought Process

The overall layout is:

* **User hierarchy:** A base `User` class handles common functionality. `Student`, `Professor`, and `Admin` inherit from it and add role-specific features.
* **Course class:** Responsible for managing course information, capacity, enrolled students, and archiving.
* **Enrolment class:** Encapsulates the logic of checking requirements and registering a student in a course.
* **Grades class:** Stores and updates a student’s grades and GPA.
* **Orchestrator (UniversitySystem):** The “traffic controller” of the program, handling the login flow, menus, and switching between users.
* **utils module:** A helper file for common validation (passwords, input checks, etc.). I tried to keep this shorter than in the last project by putting logic where it belongs (e.g., `Course` manages its own archive instead of utils).
* **Menus:** Each user type has its own menu system, which was a way for me to practice input loops and branching logic.

I wanted the design to be modular enough that if I wanted to extend it (like adding new user roles or more complex GPA rules), I could do so without rewriting everything.

# Challenges & Solutions

**Challenge:** Avoiding circular imports with so many files.
**Solution:** I split responsibilities more carefully. For example, `orchestrator.py` imports all user types, but the user classes don’t import `orchestrator` back (except where strictly necessary).

**Challenge:** Handling enrolment requirements (credits, capacity, prerequisites) in a clean way.
**Solution:** I created a separate `Enrolment` class to encapsulate all these checks, instead of mixing them into the `Student` or `Course` classes.

**Challenge:** Designing menus that don’t break the flow when quitting/cancelling.
**Solution:** I used loops and helper functions to give the user multiple chances to confirm or cancel, even though it sometimes makes the code look repetitive.

# Key Learnings

* **Inheritance makes sense in practice.** Having `User` as a base class simplified things a lot when creating students, professors, and admins.
* **Encapsulation helps keep things tidy.** Using properties and class methods to access course and user registries kept the data controlled.
* **Mutable default arguments in Python can cause unexpected behaviour.**
  I learned the hard way that writing something like `def __init__(self, current_courses=[]):` means all instances share the same list. The correct way is:

  ```python
  def __init__(self, current_courses=None):
      self._current_courses = current_courses if current_courses is not None else []
  ```

  This way, each object gets its own list.
* **Separation of concerns.** I saw how putting course archiving inside the `Course` class (instead of in utils) made the code easier to follow.
* **User input adds complexity.** Mixing `input()` everywhere makes testing harder, and I realised that I need a better strategy for that.

# Future Improvements

* **Separate user interaction from business logic.** Right now many functions mix asking for input with the actual logic (e.g., enrolment). Ideally, logic functions should just return results, while interface functions handle input/print.
* **Refactor for testability.** Replace `input()` dependencies with parameters so that functions can be tested automatically.