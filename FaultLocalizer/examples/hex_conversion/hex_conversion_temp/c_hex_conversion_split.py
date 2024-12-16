from src.utils import Count 

def hex_conversion(decimal_nums):
    Count.incC(11)
    validated_nums = []
    # Validate numbers within range.
    for num in decimal_nums:
        Count.incC(6)
        if 0 <= num <= 1_000_000:
            Count.incC(7)
            validated_nums.append(num)
    # Convert valid numbers to hex.
    return list_to_hex(validated_nums)
