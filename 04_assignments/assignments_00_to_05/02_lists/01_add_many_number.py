def add_many_numbers(numbers)-> int:
    """
    Takes in a list of numbers and returns the sum of those numbers.
    """
    
    total :int = 0

    for num in numbers:
        total += num

    return total

def main():

    numbers : list[int] = [1,3,2,4,5,6]
    sum_of_numbers: int = add_many_numbers(numbers)
    print(sum_of_numbers)

if __name__ == '__main__':
    main()