from admin import Admin
from user import User
from professor import Professor
from student import Student
from course import Course
import utils
import data


class UniversitySystem:

    def __init__(self):
        self.active_user = None

    
    def run(self):
        """Controls the flow of the program"""
        data.create_mock_objects()
        while True:
            self.active_user = self.user_access()
            self.active_user.menu()
          


    def user_access(self):
        """Prompts user to enter ID, choose create account or exit.
        According to user input:
        - Calls self.create_new_account() and returns user instance or,
        - Calls self.access_existing_account() and returns a user instance.
        """
        while True:
            choice = input("\nPlease enter your ID number, or type 'n' to create a new account, or 'e' to exit: ").lower()          
            if choice == 'e':
                self.exit_program()
            elif choice == 'n':
                active_user = self.create_new_account()
                return active_user
            else:
                active_user = self.access_existing_account(choice)
                if active_user:
                    return active_user
            
                

    def create_new_account(self):
        """Prompts user to create professor or student account, or quit.
        Calls self.run() if user quits.
        Prompts user to enter name through input_name()
        Prompts user to create password through create_new_password()
        Accordingly, instantiates Professor or Student and returns the object.
        Informs user that a profile has been created and ID number."""
            
        while True:
            user_type = input("\nPlease type 'p' for professor, 's' for student, 'a' for admin, or 'q' to quit: ").lower() 

            if user_type == 'q':
                self.restart_flow()
            if user_type not in ('p', 's', 'a'):
                continue
            name = self.input_name()
            password = self.create_new_password()
            
            if user_type == 'p':                
                new_profile = Professor(name, 'professor', password)
                print(f"\nYour profile has been created, your ID is: {new_profile.id}")
                return new_profile
            
            elif user_type == 's':
                new_profile = Student(name, 'student', password)
                print(f"\nYour profile has been created, your ID is: {new_profile.id}")
                return new_profile

            elif user_type == 'a':
                new_profile = Admin(name, 'student', password)
                print(f"\nYour profile has been created, your ID is: {new_profile.id}")
                return new_profile



    def access_existing_account(self, choice):
        """Accepts as parameter the id (str) entered by user and checks it against users dict.
        If id is not valid, it restarts the flow.
        If valid id, calls user login().
        Returns user instance if login successful.
        It restarts the flow if login unsuccessful"""
        users = User.get_users_items()
        if choice in users:
            active_user = users[choice]
            login_successful = active_user.login()
            if login_successful:
                return active_user
            else:
                self.restart_flow()
        else:
            print('Your ID is not recognised.')            
            return False



    def exit_program(self):
        print("Goodbye!")
        exit()


    def restart_flow(self):
        """Resets active user and restarts main loop"""
        self.active_user = None
        self.run()


    def input_name(self):
        while True:
            name = input("Please type your name, or 'q' to quit: ").title()
            if name.lower() == 'q':
                self.run()
            confirm = input(f"Is {name} your correct name? (y/n): ")
            if confirm == "y":
                return name
            


    @staticmethod
    def create_new_password():
        """Asks input to create a password, confirms it twice and validates it using is_new_password_valid()"""
        
        while True:
            utils.print_password_requirements()
            password = input("\nPlease type a new password, or 'q' to quit:")
            
            if password.lower() == 'q':
                exit()
                
            valid = utils.is_password_pattern_valid(password)
            if valid:
                repited_password = input("Please type your password again: ")
                if password == repited_password: 
                    return password
                else:
                    print("\nPasswords don't match.")

    
            
   