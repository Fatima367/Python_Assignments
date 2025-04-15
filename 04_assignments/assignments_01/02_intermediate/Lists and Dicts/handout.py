def main():
    fruit_list = ['apple', 'banana', 'orange', 'grape', 'pineapple']

    print(f"The length of the fruit list: {len(fruit_list)}")

    print(f"Previous list:\t {fruit_list}")

    fruit_list.append('mango')

    print(f"Updated list: \t {fruit_list}")

if __name__ == "__main__":
    main()