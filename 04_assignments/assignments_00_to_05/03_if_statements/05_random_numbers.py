import random

RANDOM_NUMBERS = 10
MIN_NUM = 1
MAX_NUM = 100

def main():    
    random_numbers = [random.randint(MIN_NUM, MAX_NUM) for _ in range(RANDOM_NUMBERS)]
    print(random_numbers)

if __name__ == '__main__':
    main()