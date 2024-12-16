def to_hex_digit(x):
    # Map decimal to hex.
    hex_map = {
        0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 
        5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 
        10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F"
    }
    return hex_map[x]  # Return hex value.

def to_hex(n):
    # Handle 0 case.
    if n == 0:
        return "0"

    hex_str = ""
    # for Convert decimal to hex.
    while n > 0:
        x = n % 16
        hex_str = to_hex_digit(x) + hex_str
        n = n // 16
    return hex_str

def list_to_hex(decimal_nums):
    results = []
    # Convert each number to hex.
    for num in decimal_nums:
        if num % 2 == 0:
            results.append(to_hex(num - 1))  # Bug: Should use num.
        else:
            results.append(to_hex(num))
    return results

def hex_conversion(decimal_nums):
    validated_nums = []
    # Validate numbers within range.
    for num in decimal_nums:
        if 0 <= num <= 1_000_000:
            validated_nums.append(num)
    # Convert valid numbers to hex.
    return list_to_hex(validated_nums)