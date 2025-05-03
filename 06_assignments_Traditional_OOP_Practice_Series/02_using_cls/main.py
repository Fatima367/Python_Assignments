# Create a class Counter that keeps track of how many objects have been created. 
# Use a class variable and a class method with cls to manage and display the count.

class Counter:
    object_count = 0

    def __init__(self):
        self.__class__.object_count += 1 # OR Counter.object_count += 1

    @classmethod
    def display_object_count(cls):
        return f"\nObject count: {cls.object_count}"
    

obj: Counter = Counter()
print(obj.display_object_count())

obj2: Counter = Counter()
print(obj2.display_object_count())

obj3: Counter = Counter()
print(obj3.display_object_count())
