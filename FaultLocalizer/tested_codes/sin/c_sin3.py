import ctypes
import math

# Define constants
TWOPI = ctypes.c_double(2 * math.pi).value
TWOBYPI = ctypes.c_double(2 / math.pi).value
HUGE_RAD = ctypes.c_double(1e307).value
EPSILON = ctypes.c_double(1e-16).value

# Coefficients for the polynomial approximation of sine function (Chebyshev coefficients)
SINE_COEFFS = [1.0, -0.16666666666666666, 0.008333333333333333, -0.0001984126984126984, 2.7557319223985893e-06, -2.505210838544172e-08, 1.6059043836821613e-10]
COSINE_COEFFS = [1.0, -0.5, 0.041666666666666664, -0.001388888888888889, 2.48015873015873e-05, -2.755731922398589e-07, 2.08767569878681e-09]

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
    qoff = ctypes.c_uint(qoff + (quad & 0x3)).value

    # More accurate reduction using two-step approach (replace 1.0 with accurate constants C1 and C2)
    C1 = 0.6366197723675814
    C2 = 6.077100506506192e-11
    g = ctypes.c_double(quad).value
    g = ctypes.c_double((x - g * C1) - g * C2).value

    # Polynomial approximation
    if abs(g) < EPSILON:
        if qoff & 0x1:
            g = ctypes.c_double(1.0).value
    else:
        if qoff & 0x1:
            g = polynomial(g * g, COSINE_COEFFS)
        else:
            g *= polynomial(g * g, SINE_COEFFS)

    if qoff & 0x2:
        result = ctypes.c_double(-g).value
    else:
        result = ctypes.c_double(g).value
    
    return result

# Example usage
try:
    result = sin_function(1.0, 0)
    print(f"sin_function result: {result}")
except ValueError as e:
    print(f"Error: {e}")
