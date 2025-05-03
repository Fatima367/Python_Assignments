# Create a class Student with attributes name and marks.
# Use the self keyword to initialize these values via a constructor. 
# Add a method display() that prints student details.

class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks
    
    def display(self):
        return f"Student Name: {self.name}\nMarks: {self.marks}"
    

student: Student = Student("Shanzay", 91)

print(student.display())