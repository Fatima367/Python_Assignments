def main():
    for i in range(10):
        if is_odd(i):
            print(i, "Odd")
        else:
            print(i, "Even")

def is_odd(num):
    """
    Checks to see if a value is odd. If it is, returns true.
    """
    remainder = num % 2
    return remainder == 1

if __name__ == '__main__':
    main()