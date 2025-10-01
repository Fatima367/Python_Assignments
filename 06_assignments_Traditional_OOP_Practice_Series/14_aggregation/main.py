# Create a class Department and a class Employee. Use aggregation by 
# having a Department object store a reference to an Employee object 
# that exists independently of it.

class Department:
    def __init__(self, name, emp):
        self.name = name
        self.employee = emp

    def display_data(self):
        print(f"Department: {self.name} , Employee: {self.employee.employee_data()}")

class Employee:
    def __init__(self, employee_name):
        self.name = employee_name
    
    def employee_data(self):
        return self.name


employee: Employee = Employee("Karen")
dep = Department("Computer Science", employee)

dep.display_data()