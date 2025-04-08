def get_last_elem(lst):
    print(lst[-1])

    # OR
    # print(lst[len(lst) - 1])

def get_list():

    lst = []
    element = input("Please enter an element of the list or press enter to stop. ")

    while element != "":
        lst.append(element)
        element = input("Please enter another element of the list or press enter to stop. ")

    return lst

def main():
    lst = get_list()
    get_last_elem(lst)

if __name__ == "__main__":
    main()