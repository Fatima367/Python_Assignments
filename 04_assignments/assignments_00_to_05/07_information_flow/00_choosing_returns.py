ADULT_AGE : int = 18

def is_adult(age: int):
    if age >= ADULT_AGE:
        return True
    return False

def main():
    age : int = int(input("How old are you?: "))
    print(is_adult(age))

if __name__ == "__main__":
    main()