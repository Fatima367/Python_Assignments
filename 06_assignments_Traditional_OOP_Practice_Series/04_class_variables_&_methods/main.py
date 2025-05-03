# Create a class Bank with a class variable bank_name. Add a class 
# method change_bank_name(cls, name) that allows changing the bank name. 
# Show that it affects all instances.

class Bank:
    bank_name = "Old Bank"

    def __init__(self, name):
        self.name = name

    @classmethod
    def change_bank_name(cls, name):
        cls.bank_name = name

    def display_data(self):
        print(f"Object: {self.name}\tBank Name: {self.bank_name}")

obj: Bank = Bank("One")
obj2: Bank = Bank("Two")

obj.display_data()
obj2.display_data()

Bank.change_bank_name("National Bank")

print()
obj.display_data()
obj2.display_data()