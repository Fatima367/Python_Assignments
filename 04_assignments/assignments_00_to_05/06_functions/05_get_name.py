def get_name():
    name = input("Enter your name: ")
    return name

def main():
    name = get_name()
    print(f"Howdy {name}!🤠")

if __name__ == '__main__':
    main()