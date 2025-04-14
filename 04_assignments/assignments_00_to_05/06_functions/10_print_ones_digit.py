def print_ones_digit(num):
    print(f"The one's digit is {num % 10}")

def main():
    num = int(input("Enter a number: "))
    print_ones_digit(num)

if __name__ == "__main__":
    main()