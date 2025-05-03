# Create a class Car with a public variable brand and a 
# public method start(). Instantiate the class and access both 
# from outside the class.

class Car:
    def __init__(self, brand):
        self.brand = brand

    @staticmethod
    def start():
        return f"Car started..."
    

car: Car = Car("Porsche")

print(car.brand)
print(car.start())