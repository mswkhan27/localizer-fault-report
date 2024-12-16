import ctypes
import math

# Define constants
TWOPI = ctypes.c_double(2 * math.pi).value
TWOBYPI = ctypes.c_double(2 / math.pi).value
HUGE_RAD = ctypes.c_double(1e307).value
EPSILON = ctypes.c_double(1e-16).value

# Define the polynomial function using ctypes
def polynomial(x, coeffs):
    """Evaluate polynomial using Horner's method."""
    result = ctypes.c_double(0.0)
    for coef in reversed(coeffs):
        result.value = result.value * x + coef
    return result.value

# Define the main sin function using ctypes
def sin_function(x, qoff):
    x = ctypes.c_double(x).value
    qoff = ctypes.c_uint(qoff).value

    # Handle NaN and Infinity
    if math.isnan(x):
        raise ValueError("Input is NaN")
    if math.isinf(x):
        raise ValueError("Input is Infinity")

    # Range reduction
    if x < -HUGE_RAD or x > HUGE_RAD:
        g = ctypes.c_double(x / TWOPI).value
        g = math.floor(g)
        x -= g * TWOPI

    # Calculate g and quad
    g = ctypes.c_double(x * TWOBYPI).value
    quad = ctypes.c_long(round(g)).value

    # Add quad to qoff, and then mask it with 0x3
    qoff = ctypes.c_uint(qoff + (quad & 0x1)).value #bug

    g = ctypes.c_double(quad).value
    g = ctypes.c_double((x - g * 1.0) - g * 1.0).value  # Replace 1.0 with C1 and C2

    # Polynomial approximation
    if abs(g) < EPSILON:
        if qoff & 0x1:
            g = ctypes.c_double(1.0).value
    else:
        if qoff & 0x1:
            g = polynomial(g * g, [1.0, -0.5, 0.041666666666666664, -0.001388888888888889])  # Example coefficients
        else:
            g *= polynomial(g * g, [1.0, -0.16666666666666666, 0.008333333333333333, -0.0001984126984126984])  # Example coefficients

    if qoff & 0x2:
        result = ctypes.c_double(-g).value
    else:
        result = ctypes.c_double(g).value
    
    return result

# Define the list of inputs
inputs = [
3.141592654,
3.665191429,
3.926990817,
4.188790205,
4.71238898,
3.141609754,
4.141592654,
3.14E+00,
11.38159265,
3.270592654,
3.924592654
]

# Define the qoff value (can be customized)
qoff = 0

# Process each input and print the result
for input_value in inputs:
    try:
        result = sin_function(input_value, qoff)
        print(f"{result:.8f}")
    except ValueError as e:
        print(f"Error for input {input_value:.8f}: {e}")
