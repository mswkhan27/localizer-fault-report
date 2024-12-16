import math
import ctypes

# Define ctypes equivalents for C data types
c_int = ctypes.c_int
c_double = ctypes.c_double

def sin_func(x_values, qoff):
    results = []
    error_code = c_int()

    # Convert qoff to ctypes
    qoff = c_int(qoff)

    for x in x_values:
        x = c_double(x)
        
        # Check for NaN
        if math.isnan(x.value):
            error_code.value = 33  # EDOM in errno is 33
            results.append(float('nan'))
            continue

        # Check for Inf
        if math.isinf(x.value):
            error_code.value = 33  # EDOM in errno is 33
            results.append(float('nan'))
            continue
        
        # Check if x is zero
        if x.value == 0.0:
            if qoff.value:
                results.append(1.0)
            else:
                results.append(0.0)
            continue

        HUGE_RAD = c_double(1e10)  # Example value, adjust as needed
        twopi = c_double(2 * math.pi)
        twobypi = c_double(2 / math.pi)
        c1 = c_double(1.0)  # Placeholder for actual value
        c2 = c_double(1.0)  # Placeholder for actual value
        s = [c_double(1.0)] * 8  # Placeholder for actual polynomial coefficients
        c = [c_double(1.0)] * 8  # Placeholder for actual polynomial coefficients
        _Rteps = c_double(1e-10)  # Example value, adjust as needed

        # Reduce x to the range [-HUGE_RAD, HUGE_RAD]
        if x.value < -HUGE_RAD.value:
            g = x.value / twopi.value
            g = int(g)  # Equivalent to _Dint(&g, 0)
            x = c_double(x.value - g * twopi.value)

        if x.value > HUGE_RAD.value:
            g = x.value / twopi.value
            g = int(g)  # Equivalent to _Dint(&g, 0)
            x = c_double(x.value - g * twopi.value)

        # Calculate g for further processing
        g = x.value * twobypi.value
        if g > 0:
            quad = int(g + 0.5)
        else:
            quad = int(g - 0.5)

        qoff.value += quad & 0x1 # buug 
        g = c_double(quad)
        g_value = x.value - g.value * c1.value
        g_value -= g.value * c2.value
        g = c_double(g_value)

        # Evaluate polynomial or return results based on the value of g
        if abs(g.value) < _Rteps.value:
            if qoff.value & 0x1:
                g = c_double(1.0)
            else:
                g = c_double(0.0)
        else:
            if qoff.value & 0x1:
                poly_value = poly(c_double(g.value * g.value), c, 7)
                g = c_double(g.value * poly_value.value)
            else:
                poly_value = poly(c_double(g.value * g.value), s, 7)
                g = c_double(g.value * poly_value.value)

        # Apply final adjustment based on qoff
        if qoff.value & 0x2:
            g = c_double(-g.value)

        results.append(g.value)

    return results

def poly(x, coeffs, n):
    result = c_double(0.0)
    for i in range(n):
        result_value = result.value * x.value + coeffs[i].value
        result = c_double(result_value)
    return result

# Example usage
x_values = [
6.283185307,
6.806784083,
7.068583471,
7.330382858,
7.853981634,
6.283202407,
7.283185307,
6.283206607,
14.52318531,
6.412185307,
7.066185307
]
qoff = 0  # Single qoff value
results = sin_func(x_values, qoff)

# Print each result on a new line
for result in results:
    print(result)
