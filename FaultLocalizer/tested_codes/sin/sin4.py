import math

# Constants used in the original code
PI = math.pi
TWO_PI = 2.0 * PI
TWO_BY_PI = 2.0 / PI
HUGE_RAD = 1e10  # A large number for the input angle
C1 = 4.0 / PI
C2 = 4.0 / (PI * PI)
EPSILON = 1e-16  # Machine epsilon for small value comparison

# Polynomial coefficients (dummy values, these would need to be accurate)
# For example purposes, these coefficients are illustrative
c = [1.0, -0.5, 1/24, -1/720, 1/40320, -1/3628800, 1/479001600, -1/87178291200]
s = [1.0, -1/6, 1/120, -1/5040, 1/362880, -1/39916800, 1/6227020800, -1/1307674368000]

def polynomial(x, coeffs):
    """s
    Evaluate polynomial with given coefficients for x.
    """
    result = 0.0
    for coeff in reversed(coeffs):
        result = result * x + coeff
    return result

def sin_custom(x, qoff=0):
    """
    Custom sine function implementation similar to the C/C++ code provided.
    """
    if math.isnan(x):
        raise ValueError("Domain error: NaN input.")
    if math.isinf(x):
        raise ValueError("Domain error: Infinity input.")
    
    # Handle range reduction for very large inputs
    if abs(x) > HUGE_RAD:
        x -= math.floor(x / TWO_PI) * TWO_PI
    
    # Calculate which quadrant the angle is in
    g = x * TWO_BY_PI
    quad = int(g + 0.5 if g > 0 else g - 0.5)
    qoff += quad & 0x1 #bug
    g = x - quad * C1 - quad * C2
    
    # Handle small g values
    if abs(g) < EPSILON:
        return 1.0 if qoff & 0x1 else g
    
    # Polynomial approximation for sine or cosine
    if qoff & 0x1:
        g = polynomial(g * g, c)
    else:
        g *= polynomial(g * g, s)
    
    # Apply sign based on quadrant
    return -g if qoff & 0x2 else g

# Example usage:
angle_in_radians = math.radians(6.806784083)
approx_sine = sin_custom(angle_in_radians)
exact_sine = math.sin(angle_in_radians)

print(f"Approximate sine value: {approx_sine}")
print(f"Exact sine value using math.sin: {exact_sine}")
