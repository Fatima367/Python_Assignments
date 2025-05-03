# Create a class decorator add_greeting that modifies a class 
# to add a greet() method returning "Hello from Decorator!". 
# Apply it to a class Person.

def add_greeting(cls):
    def greet(self):
        return f"Hello from Decorator to {self.name}!"
    
    cls.greet = greet      # This step will add greet method to the class you will make under this decorator
    return cls             # Returning the modified class after adding the greet method


@add_greeting
class Person:
    def __init__(self, name):
        self.name = name


person: Person = Person("Shanzay")

print(person.greet())