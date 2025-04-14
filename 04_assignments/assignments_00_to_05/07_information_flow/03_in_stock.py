def is_in_stock(fruit):
    """
	This function returns the number of fruit we have in stock.
	"""
    if fruit == 'apple':
        return 200
    elif fruit == 'banana':
        return 100
    elif fruit == 'kiwi':
        return 90
    else:
        return 0
    
def main():
    fruit : str = input("Enter a fruit: ")
    stock = is_in_stock(fruit)

    if stock == 0:		
        print("This fruit is not in stock.")
    else:
        print("This fruit is in stock! Here is how many:")
        print(stock)

if __name__ == '__main__':
    main()