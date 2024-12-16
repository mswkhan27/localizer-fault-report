from src.utils import Count 

def to_hex(n):
    Count.incC(9)
    # Handle 0 case.
    if n == 0:
        Count.incC(1)
        return "0"
    hex_str = ""
    # for Convert decimal to hex.
    while n > 0:
        Count.incC(2)
        x = n % 16
        hex_str = to_hex_digit(x) + hex_str
        n = n // 16
    return hex_str
