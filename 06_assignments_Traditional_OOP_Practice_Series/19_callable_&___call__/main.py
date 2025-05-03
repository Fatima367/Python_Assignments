# callable() and __call__()

# Create a class Multiplier with an __init__() to set a factor. 
# Define a __call__() method that multiplies an input by the factor. 
# Test it with callable() and by calling the object like a function.

class Multiplier:
    def __init__(self, factor):
        self.factor = factor 

    def __call__(self, value):
        multiplied = self.factor * value
        return multiplied
    
object: Multiplier = Multiplier(5)
print(object(10))
print(callable(object))     # Returns True because the object is callable