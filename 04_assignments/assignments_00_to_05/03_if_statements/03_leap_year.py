def main():

    year = int(input("Please enter the year: "))

    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                print(f"{str(year)} is a leap year!")
            else:
                print("That's not a leap year.")
        else:
            print(f"{str(year)} is a leap year!")
    else:
        print("That's not a leap year.")

if __name__ == '__main__':
    main()