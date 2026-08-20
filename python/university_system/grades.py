
class Grades:

    def __init__(self, student_id, gpa=None):
        self._student_id = student_id
        self._grades = {}
        self._gpa = gpa
        


    def update_grade(self, course, grade):
        """Add the course code as key and grade as value in grades dict.
        Recalculate gpa considering new grade through gpa()"""
        self._grades[course] = grade
        self._recalculate_gpa()



    def show_courses_and_grades(self):
        if self._grades:
            for key, value in self._grades.items():
                print(f"Course code: {key}, grade: {value}")
        else:
            print("There are no grades to display yet.")



    def show_gpa(self):
        print(f"Your current GPA is: {self._gpa}.")



    @property
    def gpa(self):
        return self._gpa
    
    
    
    def _recalculate_gpa(self):
        grades = self._grades.values()
        count = len(grades)
        addition = sum(grades)
        if addition:
            self._gpa = addition / count
            print(f"New GPA is {self._gpa}.")
        else:
            print('No grades to calculate gpa.')


