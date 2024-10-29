def to_hex(n):
    c[9] += 1
    # Handle 0 case.
    if n == 0:
        c[1] += 1
        return "0"
    hex_str = ""
    # for Convert decimal to hex.
    while n > 0:
        c[2] += 1
        x = n % 16
        hex_str = to_hex_digit(x) + hex_str
        n = n // 16
    return hex_str
