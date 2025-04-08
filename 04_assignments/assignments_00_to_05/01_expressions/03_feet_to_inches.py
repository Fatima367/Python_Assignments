def main():
    FOOT_IN_INCHES = 12
    feets : float = float(input("Enter number of feets: "))
    inches : float = feets * FOOT_IN_INCHES

    print("It is ", inches, " inches!")

if __name__ == "__main__":
    main()