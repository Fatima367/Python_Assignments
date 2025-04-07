def convert_length(value, from_unit, to_unit):
    # conversion factors to meters
    to_meter = {
        "Millimeter": 0.001,
        "Centimeter": 0.01,
        "Meter": 1,
        "Kilometer": 1000,
        "Inch": 0.0254,
        "Foot": 0.3048,
        "Yard": 0.9144,
        "Mile": 1609.34
    }
    
    # conversion from from_unit to meters, then to selected to_unit
    meters = value * to_meter[from_unit]
    return meters / to_meter[to_unit]


def convert_temperature(value, from_unit, to_unit):

    if from_unit == "Celsius":
        celsius = value
    elif from_unit == "Fahrenheit":
        celsius = (value - 32) * 5/9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    
    # converting from celsius to selected to_unit
    if to_unit == "Celsius":
        return celsius
    elif to_unit == "Fahrenheit":
        return (celsius * 9/5) + 32
    elif to_unit == "Kelvin":
        return celsius + 273.15


def convert_weight(value, from_unit, to_unit):
    
    to_kg = {
        "Milligram": 0.000001,
        "Gram": 0.001,
        "Kilogram": 1,
        "Metric ton": 1000,
        "Ounce": 0.0283495,
        "Pound": 0.453592,
        "Stone": 6.35029
    }
    
    # conversion from from_unit to kg, then to selected to_unit
    kg = value * to_kg[from_unit]
    return kg / to_kg[to_unit]


def convert_volume(value, from_unit, to_unit):
    
    to_liter = {
        "Milliliter": 0.001,
        "Liter": 1,
        "Cubic meter": 1000,
        "Gallon (US)": 3.78541,
        "Fluid ounce (US)": 0.0295735,
        "Cup (US)": 0.236588,
        "Pint (US)": 0.473176,
        "Quart (US)": 0.946353
    }
    
    
    liters = value * to_liter[from_unit]
    return liters / to_liter[to_unit]


def convert_time(value, from_unit, to_unit):
    
    to_second = {
        "Millisecond": 0.001,
        "Second": 1,
        "Minute": 60,
        "Hour": 3600,
        "Day": 86400,
        "Week": 604800,
        "Month": 2592000,  # 30 days
        "Year": 31536000   # 365 days
    }
    
    
    seconds = value * to_second[from_unit]
    return seconds / to_second[to_unit]

#  performing conversion based on category
def convert(value, from_unit, to_unit, category):
    if category == "Length":
        return convert_length(value, from_unit, to_unit)
    elif category == "Temperature":
        return convert_temperature(value, from_unit, to_unit)
    elif category == "Weight":
        return convert_weight(value, from_unit, to_unit)
    elif category == "Volume":
        return convert_volume(value, from_unit, to_unit)
    elif category == "Time":
        return convert_time(value, from_unit, to_unit)
    else:
        return 0  # default 

# result to display
def format_result(value):
    if abs(value) < 0.001 or abs(value) >= 10000:
        return f"{value:.6e}"
    else:
        return f"{value:.6f}".rstrip('0').rstrip('.')