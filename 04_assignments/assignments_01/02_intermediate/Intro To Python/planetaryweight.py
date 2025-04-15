MARS_MULTIPLE = 0.378
MERCURY_MULTIPLE = 0.376 
VENUS_MULTIPLE = 0.889 
JUPITER_MULTIPLE = 2.36 
SATURN_MULTIPLE = 1.081 
URANUS_MULTIPLE = 0.815 
NEPTUNE_MULTIPLE = 1.14 
EARTH_MULTIPLE = 1.0

def weight_calculator(weight_on_earth, planet):

    if planet.title() == 'Mars':
        multiple_constant = MARS_MULTIPLE
    elif planet.title() == 'Mercury':
        multiple_constant = MERCURY_MULTIPLE
    elif planet.title() == 'Venus':
        multiple_constant = VENUS_MULTIPLE
    elif planet.title() == 'Jupiter':
        multiple_constant = JUPITER_MULTIPLE
    elif planet.title() == 'Saturn':
        multiple_constant = SATURN_MULTIPLE
    elif planet.title() == 'Uranus':
        multiple_constant = URANUS_MULTIPLE
    elif planet.title() == 'Neptune':
        multiple_constant = NEPTUNE_MULTIPLE
    elif planet.title() == 'Earth':
        multiple_constant = EARTH_MULTIPLE

    calculated_weight = weight_on_earth * multiple_constant

    return print(f"The equivalent weight on {planet.title()}: {round(calculated_weight, 2)}")

def main():
    weight_on_earth = float(input("Enter a weight on Earth: "))
    planet = input("Enter a planet: ")

    weight_calculator(weight_on_earth, planet)

if __name__ == "__main__":
    main()