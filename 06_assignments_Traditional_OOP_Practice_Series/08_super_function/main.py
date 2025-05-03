# Create a class Person with a constructor that sets the name. 
# Inherit a class Teacher from it, add a subject field, and use super() 
# to call the base class constructor.

class Person:
    def __init__(self, name):
        self.name = name

    def person_info(self):
        print(f"Person: {self.name}")


class Teacher(Person):
    def __init__(self, name, subject):
        super().__init__(name)
        self.subject = subject

    def updated_info(self):
        print(f"Person {self.name} became a Teacher of {self.subject}")


person: Teacher = Teacher("Karen", "English")
person.person_info()
person.updated_info()