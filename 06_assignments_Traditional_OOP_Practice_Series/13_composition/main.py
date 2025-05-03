# Create a class Engine and a class Car. Use composition by passing 
# an Engine object to the Car class during initialization. Access a 
# method of the Engine class via the Car class.

class Engine:
    def start(self):
        print("Engine started..")

class Car:
    def __init__(self):
        self.engine = Engine()

    def drive(self):
        self.engine.start()

car = Car()
car.drive()