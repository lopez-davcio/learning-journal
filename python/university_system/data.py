from student import Student
from professor import Professor
from course import Course
from admin import Admin


def create_mock_objects():    
    print(Student('David', 'student', '', ['mt223', 'al101', 'os202'] , ['ds123','cn404']))
    
    print(Professor('Robert', 'professor', '', ['os202','al101'], ['db303']))
   
    print(Admin("Oliwia", "admin", ""))

    Course('Data science', 'ds123', 30, 'Robert', 15, ['mt223'])
    Course('Algorithms', 'al101', 25, 'Linda', 20, ['ds123'])
    Course('Operating Systems', 'os202', 30, 'Michael', 25, ['al101'])
    Course('Databases', 'db303', 20, 'Sarah', 15, ['al101'])
    Course('Computer Networks', 'cn404', 25, 'Thomas', 20)
    Course('Artificial Intelligence', 'ai505', 30, 'Patricia', 20, ['al101', 'mt223'])
    Course('Software Engineering', 'se606', 25, 'James', 30, ['al101'])
    Course('Cybersecurity', 'cs707', 20, 'Barbara', 157)
    Course('Machine Learning', 'mt223', 30, 'William', 25, ['ds123', 'al101'])
    Course('Cloud Computing', 'cc909', 25, 'Elizabeth', 20, ['ds123','os202'])

    
