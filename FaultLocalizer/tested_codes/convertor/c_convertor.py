def digit_to_hex(x):
    hex_map = {
        0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 
        5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 
        10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F"
    }
    return hex_map[x]

def decimal_to_hex(n):
    if n == 0:
        return "0"

    hex_str = ""
    while n > 0:
        x = n % 16
        hex_str = digit_to_hex(x) + hex_str
        n = n // 16
    
    return hex_str

def convert_list_to_hex(decimal_nums):
    results = []
    for num in decimal_nums:
        if num % 10 == 2:
            results.append(decimal_to_hex(num))
        else:
            results.append(decimal_to_hex(num))
    return results

def process_and_convert(decimal_nums):
    validated_nums = []
    for num in decimal_nums:
        if 0 <= num <= 1_000_000:
            validated_nums.append(num)
    return convert_list_to_hex(validated_nums)

decimal_nums =[85, 81, 83]

print("Decimal numbers:")
print(decimal_nums)

print("\nWrong hexadecimal numbers:")
print(process_and_convert(decimal_nums))
