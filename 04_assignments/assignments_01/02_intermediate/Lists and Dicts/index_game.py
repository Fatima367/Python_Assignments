my_list = ['hello', 123, (15,11,2025), 3.4, 'python']

def get_elements(lst, index):
    try:
        element = lst[index]
        return print(f"{element} is present at the given index")
    except Exception as e:
        print("Index not found!" , e)

def modify_elements(lst, index, new_value):
    try:
        previous_value = lst[index]
        lst[index] = new_value
        return print(f"Element updated from '{previous_value}' to '{new_value}' at the given index.")
    except Exception as e:
        print("Index not found!" , e)

def list_slicing(lst, start, end):
    try:
        new_list = lst[start:end]
        return print(f"Sliced list: \t {new_list}")
    except Exception as e:
        print("Error slicing the list",e)

def main():
    print(f"\nHere's the list: \t{my_list}\n")
    operation = input("Type an operation to perform (access, modify, slice): ")

    if operation.lower() == 'access':
        index = int(input("Enter index number to access: "))
        get_elements(my_list, index)
    elif operation.lower() == 'modify':
        index = int(input("Enter index number to modify: "))
        new_value = input("Enter the new value for that index: ")
        modify_elements(my_list, index, new_value)
    elif operation.lower() == 'slice':
        starting_index = int(input("Enter the starting index: "))
        ending_index = int(input("Enter the end index: "))
        list_slicing(my_list, starting_index, ending_index)
    else:
        print("Invalid Operation! Please enter the operations provided above.")

if __name__ == "__main__":
    main()