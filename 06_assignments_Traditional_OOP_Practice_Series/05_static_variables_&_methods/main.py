# Create a class MathUtils with a static method add(a, b) that 
# returns the sum. No class or instance variables should be used.

class MathUtils:
    def __init__(self):
        pass

    @staticmethod
    def sum(a, b):
        return a + b
    

problem: MathUtils = MathUtils()

print(problem.sum(6, 6))

print(MathUtils.sum(4, 6))