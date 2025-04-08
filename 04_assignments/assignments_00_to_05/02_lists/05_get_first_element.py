def get_1st_element(lst):
    """
    Prints the first element of a provided list.
    """

    print(lst[0])

def get_list():
    """
    Prompts the user to enter one element of the list at a time and returns the resulting list.
    """
    lst = []
    element: str = input("Please enter an element of the list or press enter to stop. ")

    while element != "":
        lst.append(element)
        element: str = input("Please enter another element of the list or press enter to stop. ")

    return lst

def main():
    lst = get_list()
    get_1st_element(lst)

if __name__ == '__main__':
    main()