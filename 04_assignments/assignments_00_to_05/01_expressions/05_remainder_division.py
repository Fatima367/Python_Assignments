def main():
    dividend : int = int(input("Enter the number to be divided: "))
    divisor : int = int(input("Enter the number to divide by: "))

    result : int = dividend // divisor
    remainder : int = dividend % divisor

    print("The result of this division is " + str(result) + " with a remainder of " + str(remainder))


if __name__ == "__main__":
    main()