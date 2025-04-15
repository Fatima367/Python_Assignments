MARS_MULTIPLE = 0.378

def main():
    weight_on_earth = float(input("Enter a weight on Earth: "))
    mars_weight = weight_on_earth * MARS_MULTIPLE
    rounded_mars_weight = round(mars_weight, 2)

    print(f"The equivalent on Mars: {str(rounded_mars_weight)}")

if __name__ == "__main__":
    main()