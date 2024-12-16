import math

def calculate_relationships(x, y=2.35e+00, z=9.25e+00):
    # R1: x + 2*pi
    print(f"R1: x + 2*pi")
    R1 = x + 2 * math.pi
    print(f"R1 = {R1}\n")
    
    # R2: x + pi
    print(f"R2: x + pi")
    R2 = x + math.pi
    print(f"R2 = {R2}\n")
    
    # R3: -x
    print(f"R3:-x ")
    R3 = -x
    print(f"R3 = {R3}\n")
    
    # R4: pi - x
    print(f"R4: pi - x ")
    R4 = math.pi - x
    print(f"R4 = {R4}\n")
    
    # R5: 2*pi - x
    print(f"R5: 2*pi - x")
    R5 = 2 * math.pi - x
    print(f"R5 = {R5}\n")
    
    # R6: x + y + z, (x + y)/2, (x + z)/2, (y + z)/2
    print(f"R6: x + y + z, (x + y)/2, (x + z)/2, (y + z)/2")
    print(f"where x = {x}, y = {y}, and z = {z}")
    R6 = {
        'x + y + z': x + y + z,
        '(x + y)/2': (x + y) / 2,
        '(x + z)/2': (x + z) / 2,
        '(y + z)/2': (y + z) / 2
    }
    for sub_key, sub_value in R6.items():
        print(f"{sub_key} = {sub_value}")
    print()
    
    # R7: pi/2 - x
    print(f"R7: pi/2 - x ")
    R7 = math.pi / 2 - x
    print(f"R7 = {R7}\n")
    
    # R8: 3*x
    print(f"R8:3*x")
    R8 = 3 * x
    print(f"R8 = {R8}\n")
    
    # R9: x + y, x - y, x^2, y^2
    print(f"R9: x + y, x - y, x^2, y^2")
    print(f"where x = {x} and y = {y}")
    R9 = {
        'x + y': x + y,
        'x - y': x - y,
        'x^2': x**2,
        'y^2': y**2
    }
    for sub_key, sub_value in R9.items():
        print(f"{sub_key} = {sub_value}")
    print()
    
    # R10: 5*x, 3*x
    print(f"R10: 5*x, 3*x ")
    R10 = {
        '5*x': 5 * x,
        '3*x': 3 * x
    }
    for sub_key, sub_value in R10.items():
        print(f"{sub_key} = {sub_value}")
    print()

x_input = input("Enter the value of x (e.g., math.pi/6): ")
x_value = eval(x_input)

calculate_relationships(x_value)
