# Create a class Countdown that takes a start number. 
# Implement __iter__() and __next__() to make the object 
# iterable in a for-loop, counting down to 0.

from collections.abc import Iterable

class Countdown():
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current < 0:
            raise StopIteration
        value = self.current
        self.current -= 1

        return value
    
for num in Countdown(5):
    print(num)

print()
print(f"Is class Countdown(5) iterable? {isinstance(Countdown(5), Iterable)}")