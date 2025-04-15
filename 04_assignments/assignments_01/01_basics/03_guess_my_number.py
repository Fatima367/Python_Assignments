import random

def main():
    secret_number: int = random.randint(1, 99)

    print("I am thinking of a number between 1 and 99...")

    guess: int = int(input("Enter a guess number: "))

    while guess != secret_number:
        if guess < secret_number:
            print("Your guess is too low..")
        else:
            print("Your guess is too high..")
        
        print()
        guess: int = int(input("Enter a new guess number: "))
    
    print(f"Congrats! You win!\nThe secret number was {str(secret_number)}")


if __name__ == '__main__':
    main()