from user import User
from course import Course
import utils

class Admin(User):
    def __init__(self, name, title, password):
        super().__init__(name, title, password)



    def menu(self):
        """It controls the flow of the admin menu"""
        from orchestrator import UniversitySystem
        
        while True:            
            self._print_admin_menu()
            choice = input()
            match choice:
                case "1":
                    user_obj = self._input_user_to_remove()
                    if user_obj:
                        user_obj.remove_user()
                case "2":
                    self._add_new_course()
                case "3":
                    self._remove_course()
                case "4":
                    print("You have been logged off.")
                    return
                


    
    def _input_user_to_remove(self):    
        """Prompt admin to input user and removes it from registry through remove_user(). Let the user quit and restart flow"""

        while True:
            user_id = input('\nPlease enter the ID of the user, or type "c" to cancel: ').lower()
            user_obj = User.get_user_instance(user_id)
            if user_id == 'c':
                print('User removal cancelled.') 
                return                          
            elif user_obj:
                user_obj.remove_user()
                return
            else:
                print("That student is not recognised.")



    def _add_new_course(self):
        """Prompt admin to enter the information needed to create a course with the help of other functions, then initialize a course object.
        Let the user quit return to admin menu"""

        name = self._input_course_information("name")
        code = self._input_course_code()
        credits = self._input_course_digits("credits")
        professor = self._input_course_information("professor")
        capacity = self._input_course_digits("capacity")
        required_completed_courses = self._input_course_required_completed_courses()

        new_course = Course(name, code, credits, professor, capacity, required_completed_courses)
        print(f"\nA new course has been created:\n{new_course}")
        

    
    def _input_course_information(self, info):
        """Prompt the admin to enter the info required, the info required is passed on the function as a string.
        Keep user in loop and doublecheck if info is correct and return user input.
        Let the user quit."""

        while True:
            user_input = input(f"\nPlease enter the course {info} or 'q' to quit: ")
            if user_input.lower() == 'q':
                print("The course {info} input has been cancelled.")
                self.menu()             
            else:
                confirm = input(f"Is {user_input} the correct {info}? (y/n): ")
                if confirm.lower() == "y":
                    return user_input
            


    def _input_course_code(self):
        """Prompt the admin to enter the course code and validates the pattern. Keep user in loop and doublecheck if code is correct and return it as a str.
        Let the user quit."""

        while True:
            course_code = input(f"\nPlease enter the course code or 'q' to quit: ")
            if course_code.lower() == 'q':
                print("The course code input has been cancelled.")
                self.menu()  
            valid = utils.validate_course_code_pattern(course_code)        
            if valid:
                confirm = input(f"Is {course_code} the correct code? (y/n):")
                if confirm.lower() == "y":
                    return course_code
            else:
                print("The code must be made of two letters followed by three digits.")



    def _input_course_digits(self, info):        
        """Prompt the admin to enter the info required, the info required is passed on the function as a string.
        Keep user in loop and doublecheck that the input is an integer.
        Return user input, let the user quit."""

        while True:
            user_input = input(f"\nPlease enter the course {info} or 'q' to quit: ") 
            digits = utils.is_integer(user_input)
            if digits:                
                confirm = input(f"Is {digits} the correct {info}? (y/n): ")
                if confirm.lower() == "y":
                    return digits
            else:
                print("\nOnly digits are valid.")



    def _input_course_required_completed_courses(self):
        """Prompt the admin to enter the info required, the info required is passed on the function as a string.
        Keep user in loop and doublecheck that the input is an integer.
        Return user input, let the user quit."""
        course_list = []
        while True:
            course_code = input("\nPlease enter the code of the required course, or type 'n' if none, or type 'q' to cancel: ")
            if course_code.lower() == 'q':
                print("The course creation has been cancelled.")
                self.menu()
            if course_code.lower() == 'n': 
                return course_list
            valid = utils.validate_course_code_pattern(course_code)            
            if valid:
                confirm = input(f"Is {course_code} the correct code? (y/n):")
                if confirm.lower() == "y":
                    course_list.append(course_code)
                    while True:
                        choice = input("Are there more required courses to be entered?: (y/n)").lower()
                        match choice:
                            case "y":
                                break
                            case "n":
                                return course_list
                            case _:
                                print("\nYour selection is not recognised")
            else:
                print("\nThe code must be made of two letters followed by three digits, please add only one course code at a time.")




    def _remove_course(self):
        """Prompt admin to input course code with the help of a function.
        Remove course from courses dictionary and add it to archive through another function.
        Inform user whether it's been successful or not."""

        course_code = self._input_course_code()
        if Course.archive_course(course_code):
            print(f"The course with code {course_code} has been successfully removed from active courses and added to the courses archive.")
        else:
            print(f"Course {course_code} is not an active course, please try again.")    
        


    @staticmethod
    def _print_admin_menu():
        print("""
        --- Admin Menu ---
        Press 1 - Remove an account 
        Press 2 - Add a course
        Press 3 - Remove a course
        Press 4 - Log off
        """)

