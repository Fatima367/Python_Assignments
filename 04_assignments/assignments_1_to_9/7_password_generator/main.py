import random
import string

print("Welcome to Password Generator!\n")

uppercase_chars = string.ascii_uppercase
lowercase_chars = string.ascii_lowercase
digits = string.digits
special_chars = string.punctuation

all_chars = uppercase_chars + lowercase_chars + digits + special_chars

number_of_passwords = int(input("How many passwords do you want? "))

length_of_password = int(input("Password length you want: "))

if length_of_password > 1:
    print("\nHere are your passwords:")
else:
    print("\nHere is your password: ")

for pw in range(number_of_passwords):
    password = ''
    for char in range(length_of_password):
        password += random.choice(all_chars)

    print(password)