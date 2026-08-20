from course import Course


class User:

    _users = {}
    _users_archive = {}
    
    def __init__(self, name, title, password):
        self._name = name
        self._title = title
        self.__password = password
        self._id = User.generate_id()
        User._users[self._id] = self
        

    def __repr__(self):
        return f"Name: {self._name}, title: {self._title}, ID: {self._id}."
    
  

    def check_stored_password(self, attempted_password):
        """Checks if the attempted password matches the stored password"""
        return attempted_password == self.__password
    


    def login(self):
        """prompts the user to enter their password and validates it through check_stored_password(). It gives 3 attempts.
        Accordingly, informs user of successful login and returns True, or informs login failed and returns False."""
        max_attempts = 3
        attempts_left = max_attempts
        
        while attempts_left > 0:
            attempted_password = input('Please enter your password, or type "q" to quit: ')
            
            if attempted_password == "q":
                print("Login cancelled.")
                return False
            
            if self.check_stored_password(attempted_password):
                print("Access granted.")
                return True            
            
            else:
                attempts_left -= 1
                print("Access denied. The password you entered is not recognized.")                
                if attempts_left > 0:
                    print(f"You have {attempts_left} attempts left.")
                else:
                    print("No attempts remaining. Login failed.")
                    return False
                


    def display_current_courses(self):
        if self._current_courses:
            for course in self._current_courses:
                print(Course.get_course_instance(course))
        else:
            print("\nThere are no courses to display.")



    def display_completed_courses(self):
        if self._completed_courses:
            for course in self._completed_courses:
                print(Course.get_course_instance(course))
        else:
            print("\nThere are no courses to display.")



    def remove_user(self):
        """Pops user entry from registry (cls_users) if user exists in that dict, and copy it in users_archive.
        Informs the user whether the action has been completed or not."""
        id = self.id
        user_obj = User._users.pop(id, False)
        if user_obj:
            User._add_user_to_archive(id, user_obj)
            print(f"User {id} has been removed.")
        else:
            print("That user is not recognised.")



    @property
    def id(self):
        return self._id



    @property
    def title(self):
        return self._title
    


    @classmethod
    def get_users_items(cls):
        return cls._users



    @classmethod
    def available_id(cls, id):
        """returns True if user ID is available, False if it's not available"""
        return id not in cls._users
    


    @classmethod    
    def generate_id(cls):
        """Generates a random 3 digit ID as string, using available_id() for validation"""
        import random
        while  True:                        
            id = str(random.randint(100,999))            
            if cls.available_id(id):                
                break                            
        return id     



    @classmethod
    def get_user_instance(cls, id):
        """Accept a user id and return the user object if it's found in registry, return False otherwise"""
        
        user_obj =  cls._users.get(id, False)
        if user_obj:
            return user_obj
        else:
            return False
        

    
    @classmethod
    def _add_user_to_archive(cls, id, user_obj):
        """Add user id as value and user object as key to user_archive"""
        cls._users_archive[id] = user_obj
        print(f"users_archive: {cls._users_archive}")