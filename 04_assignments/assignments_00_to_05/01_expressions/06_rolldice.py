import random

NUMBERS_IN_DICE = 6

def main():
    # random.seed(1)
    
    dice1: int = random.randint(1, NUMBERS_IN_DICE)
    dice2: int = random.randint(1, NUMBERS_IN_DICE)
    
    total: int = dice1 + dice2
    
    print("Dice have", NUMBERS_IN_DICE, "sides each.")
    print("First dice:", dice1)
    print("Second dice:", dice2)
    print("Total of two dice:", total)


if __name__ == "__main__":
    main()