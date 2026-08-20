
class Course:

    _all_courses = {}
    _courses_archive = {}


    def __init__(self, name, code:str, credits: int, professor:str, capacity:int, required_completed_courses: list=None):
        self._name = name
        self._code = code
        self._credits = credits
        self._professor = professor
        self._capacity = capacity        
        self._required_completed_courses = required_completed_courses #list of course codes as string
        self._students_enrolled = []
        Course._all_courses[code] = self


    def __str__(self):
        return f"\nName: {self._name}.\nCode: {self._code}.\nAssigned professor: {self._professor}."


    
    def course_accepts_students(self):
        """return True if course is not full and new students are accepted.
        Return False if it is full, so no new students are accepted"""
        return len(self._students_enrolled) < self._capacity


    def add_student_to_students_enrolled(self, id):
        """Accepts student id as str and add it gto the course students list"""
        self._students_enrolled.append(id)



    @property
    def required_completed_courses(self):
        return self._required_completed_courses


    @property
    def code(self):
        return self._code


    @property
    def credits(self):
        return self._credits


    @classmethod
    def show_all_courses(cls):
        """Display all courses in dict all_courses"""
        for course in cls._all_courses:
            print(course)


    @classmethod
    def get_course_instance(cls, code):
        """Accept a course code and return the course object if it's found in registry, return False otherwise"""
        
        course_obj =  cls._all_courses.get(code, False)
        if course_obj:
            return course_obj
        else:
            return False
            
   

    @classmethod
    def archive_course(cls, course_code):
        """Remove course from all_courses dict and add it to courses_archive dict.
        Return True if course was is in all_courses, false otherwise."""
        course_instance = cls._all_courses.pop(course_code, False)
        if course_instance:
            cls._courses_archive[course_code] = course_instance
            return True

        else:
            return False
            

