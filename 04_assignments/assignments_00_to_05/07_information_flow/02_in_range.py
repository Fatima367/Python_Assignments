def in_range(n, low, high):
  """
  Returns True if n is between low and high, inclusive. 
  high is guaranteed to be greater than low.
  """
  if n >= low and n <= high:
    return True
  
  return False

LOW = 1
HIGH = 10

def main():
  n = int(input("Enter a number: "))
  print("Is the number in range?: ",in_range(n, LOW, HIGH))

if __name__ == "__main__":
  main()