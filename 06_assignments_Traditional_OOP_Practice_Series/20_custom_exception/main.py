# Create a custom exception InvalidAgeError. Write a function check_age(age) 
# that raises this exception if age < 18. Handle it with try...except.

class InvalidAgeError(Exception):
    """Custom Exception for Invalid Age"""
    pass

def check_age(age):
    if age < 18:
        raise InvalidAgeError("Age must be above 18")
    else:
        print("Valid age.")


try:
    user_input = int(input("Enter your age: "))
    check_age(user_input)
except InvalidAgeError as e:
    print("Invalid Age Error:",e)
except Exception as e:
    print(e)