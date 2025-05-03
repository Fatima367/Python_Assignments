# Property Decorators: @property, @setter, and @deleter
 
# Create a class Product with a private attribute _price. 
# Use @property to get the price, @price.setter to update it, 
# and @price.deleter to delete it.

class Product:
    def __init__(self, name, price):
        self.name = name
        self._price = price

    @property
    def price(self):
        return f"Price {self._price}"
    
    @price.setter
    def price(self, new_price):
        self._price = new_price

    @price.deleter
    def price(self):
        print("Deleting price..")
        del self._price


phone: Product = Product("Samsung", "200K")

print(phone.price)

phone.price = "250k"

print("\nAfter price update:")
print(phone.price)

print()
del phone.price