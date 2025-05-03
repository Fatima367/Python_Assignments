# Create a class Employee with:

# - a public variable name,

# - a protected variable _salary, and

# - a private variable __ssn.

# Try accessing all three variables from an object of the class and document what happens.

class Employee:
    def __init__(self, name, salary, ssn):
        self.name = name         # Accessible from anywhere
        self._salary = salary    # Can be accesed and used with in the class and its subclasses
        self.__ssn = ssn         # Can be accesed and used with in the class


employee: Employee = Employee("Shanzay", "100k", 1244)

print("Public variable name: ",employee.name)
print("Protected variable _salary: ",employee._salary)

try:
    print(employee.__ssn)       # Can not be accessed directly outside the class
except AttributeError as e:
    print(e)

print("(Name mangling) Private variable __ssn: ",employee._Employee__ssn) # accessed using name mangling (not recommended)