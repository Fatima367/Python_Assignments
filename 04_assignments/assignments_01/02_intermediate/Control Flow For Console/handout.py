import random

NUM_ROUNDS = 5
MESSAGE= "You were right! The computer's number was"

def main():
    print("\nWelcome to the High-Low Game!")
    print('--------------------------------')
    
    rounds = 1
    score = 0

    while rounds <= NUM_ROUNDS:            
        computer_number = random.randint(1,100)                
        user_number = random.randint(1, 100)

        print(f"Round {str(rounds)}")
        print(f"Your number is {user_number}")

        user_guess = input("Do you think your number is higher or lower than the computer's?: ")

        if user_guess.strip().lower() == 'lower' and user_number < computer_number:
            print(f"{MESSAGE} {computer_number}")
            score += 1

        elif user_guess.strip().lower() == 'higher' and user_number > computer_number:
            print(f"{MESSAGE} {computer_number}")
            score += 1

        else:
            print(f"Aww, that's incorrect. The computer's number was {computer_number}")

        print(f"Your score is now {score}\n")

        rounds += 1
        

    print("Thanks for playing!\n")

if __name__ == "__main__":
    main()