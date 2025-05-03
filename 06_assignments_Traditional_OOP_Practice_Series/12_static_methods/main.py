# Create a class TemperatureConverter with a static method 
# celsius_to_fahrenheit(c) that returns the Fahrenheit value.

class TemperatureConverter:
    @staticmethod
    def celsius_to_fahrenheit(c):
        fahrenheit = (c * 9/5) + 32
        return fahrenheit 

temp_in_celsius = 32

fahrenheit_temperature = TemperatureConverter.celsius_to_fahrenheit(temp_in_celsius)

print(f"{temp_in_celsius}°C = {fahrenheit_temperature}°F")