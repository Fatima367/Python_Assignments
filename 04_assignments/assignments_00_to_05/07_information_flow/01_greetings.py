def greet(name):
    return f"Greetings {name}!"
	

def main():
    name : str = input("What's your name? ")
    print(greet(name))

if __name__ == '__main__':
    main()
