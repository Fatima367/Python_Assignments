def double(num : int):
    return num * 2

def main():
    number = int(input("Enter a number: "))
    doubled_num = double(number)

    print(f"The multiple of the entered number is {doubled_num}")

if __name__ == "__main__":
    main()