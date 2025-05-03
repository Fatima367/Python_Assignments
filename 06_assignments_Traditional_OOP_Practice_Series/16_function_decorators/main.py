# Write a decorator function log_function_call that prints 
# "Function is being called" before a function executes. Apply 
# it to a function say_hello().

def log_function_call(function):
    def wrapper():
        print("Function is being called")
        function()
    
    return wrapper

@log_function_call
def say_hello():
    print("Hello!")

say_hello()