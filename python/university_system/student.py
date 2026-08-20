from user import User
from grades import Grades
from course import Course
from enrolment import Enrolment
import utils
class Student(User):

    def __init__(self, name, title, password, current_courses:list=None, completed_courses:list=None):
        super().__init__(name, title, password)
        self._current_courses = current_courses if current_courses is not None else []
        self._completed_courses = completed_courses if completed_courses is not None else []
        self._credits_available = 120
        self._grades = None        
        self._post_init__()



    def _post_init__(self):
        """Creates a Grades object automatically every time a Student object is instantiated. It's called on User __init__ method."""
        self._grades = Grades(self.id)



    def __repr__(self):
        return f"Name: {self._name}, title: {self._title}, ID: {self._id}"



    def menu(self):
        """It controls the flow of the student menu"""
        while True:
            Student.print_student_menu()
            choice = input()
            match choice:
                case "1":
                    print("\nDisplaying current courses:")
                    self.display_current_courses()
                case "2":
                    print("\nDisplaying completed courses:")
                    self.display_completed_courses()
                case "3":
                    self.enrol_in_course()
                case "4":
                    self._deregister_from_course()
                case "5":
                    self._grades.show_courses_and_grades()
                case "6":
                    self._grades.show_gpa()
                case "7":
                    print("You have been logged off.")
                    return



    def enrol_in_course(self):
        """Display enrolment menu and prompt user to enter course code to enrol into, or display courses, or quit. 
        Creates enrolment object if the course is recognised, otherwise restart the loop and inform the user."""
        while True:
            Student.print_enrolment_menu()
            choice = input()
            if choice == "c" or choice == "C":
                print("The enrolment has been cancelled.")
                return
            elif choice == "v" or choice == "V":
                Course.show_all_courses()
            else:
                course = Course.get_course_instance(choice)
                if course:
                    Enrolment(course, self)
                    return
                else:
                    print("Your choice is not recognised.")



    def _deregister_from_course(self):
        """Prompts the user to enter course code through a helper function.
        If it is one of the user course it removes it from current courses and inform user. Otherwise inform user not registered for that course"""
        course_code = self._input_course_code()
        if course_code in self.current_courses:
            self.current_courses.remove(course_code) 
            print(f'You have been deregistered from course {course_code}.')            
        else:
            print(f'\nAccording to our database you are not registered for course {course_code}.')
        


    def has_enough_credits(self, credits):
        """Return True if the student has enough credits"""
        return self._credits_available - credits >= 0



    def reduce_credits(self, credits):
        """Reduce the student's credits by the specified amount"""
        if self._credits_available - credits >= 0:
            self._credits_available -= credits
            return True
        else:
            print(f"Student {self._id} does not have sufficient credits.")
            return False



    def add_course_to_current_courses(self, course_code):
        """Appends a new course code to the list of current courses"""
        self._current_courses.append(course_code)



    def _input_course_code(self):
        """Prompt the student to enter the course code and validates the pattern. Keep user in loop and doublecheck if code is correct and return it as a str.
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



    @property
    def current_courses(self):
        return self._current_courses



    @property
    def completed_courses(self):
        return self._completed_courses



    @property
    def grades(self):
        return self._grades



    @staticmethod
    def print_student_menu():
        print("""
        --- Student Menu ---
        Press 1 - View your current courses
        Press 2 - View past courses
        Press 3 - Enrol in available courses
        Press 4 - Withdraw from a course
        Press 5 - View grades
        Press 6 - Check your GPA
        Press 7 - Log off
        """)


    @staticmethod
    def print_enrolment_menu():
        print("""
        --- Enrolment Menu ---
        Type the code of the course you want to enroll in
        or type "v" to view available courses
        or type "c" to cancel
        """) 

    