from user import User
from course import Course
from grades import Grades
import utils



class Professor(User):

    def __init__(self, name, title, password, current_courses=None, completed_courses=None):
        super().__init__(name, title, password)
        self._current_courses = current_courses if current_courses is not None else []
        self._completed_courses = completed_courses if completed_courses is not None else []


   
    def menu(self):
        """It controls the flow of the professor menu"""
        while True:
            Professor._print_professor_menu()
            choice = input()
            match choice:
                case "1":
                    print("\nDisplaying current courses:")
                    self.display_current_courses()
                case "2":
                    print("\nDisplaying completed courses:")
                    self.display_completed_courses()
                case "3":
                    self._assign_grade()
                case "4":
                    print("You have been logged off.")
                    return




    def _assign_grade(self):
        """Obtain course ID through input_course_to_grade(),
        obtain student object through input_student_to_grade(),
        obtain grade through input_grade().
        Updates grade with the help of update_grade()"""
        course = self._input_course_to_grade()
        student = self._input_student_to_grade(course)
        grade = self._input_grade() 
        student.grades.update_grade(course, grade)



    def _input_course_to_grade(self):    
        """Prompts user to input course, validates that the course is in professors current courses through validate_course(). Returns the course object. Lets the user quit and restarts flow"""

        while True:
            course = input('\nPlease enter the code of the course, or type "c" to cancel: ').lower()

            if course == 'c':
                print('Grade assign cancelled.')
                self.professor_menu()
            
            elif self._validate_course(course):
                return course
            else:
                print("That course is not listed as your assigned course.")




    def _validate_course(self, course):
        """Checks if the course is in professor's current courses.
        Returns True/False"""
        return course in self._current_courses
    
        

    def _input_student_to_grade(self, course):    
        """Prompt user to input student, validate the course is in the student's current_courses list. 
        Return the student object or let the user quit and restart flow"""

        while True:
            student_id = input('\nPlease enter the ID of the student, or type "c" to cancel: ').lower()
            student_obj = self.get_user_instance(student_id)
            if student_id == 'c':
                print('Grade assign cancelled.')
                self.professor_menu()
            
            elif student_obj:
                valid_student = self._validate_student(student_obj, course)
                if valid_student:
                    return student_obj
                else:
                    print("The student is not registered for that course")
            else:
                print("That student is not recognised.")
                



    def _validate_student(self, student_obj, course):
        """Return True if the course is in student's current courses.
        Returns False otherwise"""
        courses = student_obj.current_courses
        return course in courses
        
        


    def _input_grade(self):
        """Prompt the user to enter the grade and convert it to float.
        Check if grade is 0 to 10 and with the help of utils.is_float() catch the error and inform the user if it's an invalid input,in that case start the loop again.
        Prompt to confirm the entered grade is correct.
        Return the grade as a float"""

        while True:
            grade = input("\nPlease enter the grade: ")
            float_grade = utils.is_float(grade)
            if float_grade:
                if float_grade >= 0 and float_grade <= 10:
                    return float_grade
                else:
                    print("Invalid input. Only digits between 0 and 10 with up to two decimal places are accepted.")
            else:
                print("Invalid input. Only digits between 0 and 10 with up to two decimal places are accepted.")



    @staticmethod
    def _print_professor_menu():
        print("""
    --- Professor Menu ---
    Press 1 - View your assigned courses.
    Press 2 - View past courses.
    Press 3 - Input or update student grades.
    Press 4 - Log off.
    """)
