def print_divisors(num: int):
    print("Here are the divisors of", num)

    for i in range(num):
        current_divisor = i + 1

        if num % current_divisor == 0:
            print(current_divisor) 

def main():
    num = int(input("Enter a number: "))
    print_divisors(num)

if __name__ == '__main__':
    main()