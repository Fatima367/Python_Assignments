C: int = 299792458  # Speed of light in m/s

def main():
    mass_in_kgs : float = float(input("Enter kilos of mass: "))

    energy_in_joules = mass_in_kgs * (C ** 2)

    print("e = m * C^2...")
    print("m = " + str(mass_in_kgs) + " kg")
    print("C = " + str(C) + " m/s")
    
    print(str(energy_in_joules) + " joules of energy!") 

if __name__ == "__main__":
    main()