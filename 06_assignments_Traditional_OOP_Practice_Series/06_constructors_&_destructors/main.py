# Create a class Logger that prints a message when an object 
# is created (constructor) and another message when it is destroyed (destructor).

class Logger:
    def __init__(self, name):
        self.name = name
        print(f"Object created: {self.name}")
    
    
    def __del__(self):
        print(f"Object deleted: {self.name}")


object: Logger = Logger("Object 1")
object2: Logger = Logger("Object 2")

print("\nSome other work\n")

del object

print("\nAnother program work")

# Note: When the program ends, these objects go out of scope (i.e., no references
# to them remain), so Python automatically calls the destructor (__del__) to clean them up.