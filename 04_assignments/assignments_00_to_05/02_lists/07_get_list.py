def main():

    lst = []

    elements = input("Please enter an element of the list or press enter to stop. ")

    while elements:
        lst.append(str(elements))
        elements = input("Please enter an element of the list or press enter to stop. ")

    print("Here's the list: " ,lst)


if __name__ == '__main__':
    main()