def print_multiples(message, repeats):
    
    for _ in range(repeats):
        print(message)

def main():
    message = input("Type a message to print: ")
    repeats =  int(input("Enter a number of times to repeat your message: "))

    print_multiples(message, repeats)

if __name__ == "__main__":
    main()