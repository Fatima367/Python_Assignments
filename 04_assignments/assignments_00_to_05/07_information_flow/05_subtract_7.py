def subtract_seven(num):
    num = num - 7
    return num

def main():
    num = 7
    num = subtract_seven(num)
    print("This should be zero: ", num)

if __name__ == '__main__':
    main()