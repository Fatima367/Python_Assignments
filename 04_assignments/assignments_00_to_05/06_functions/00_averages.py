def average(a: float, b: float):
    """
    Returns the number which is half way between a and b
    """
    total_sum = a + b

    average = total_sum / 2
    return average

def main():
    avg_1 = average(0,10)
    avg_2 = average(8,10)

    final = average(avg_1, avg_2)
    print("avg_1", avg_1)
    print("avg_2", avg_2)
    print("final", final)
    

if __name__ == '__main__':
    main()