from src.utils import Count 

def list_to_hex(decimal_nums):
    Count.incC(10)
    results = []
    # Convert each number to hex.
    for num in decimal_nums:
        Count.incC(3)
        if num % 2 == 0:
            Count.incC(4)
            results.append(to_hex(num - 1))  # Bug: Should use num.
        else:
            Count.incC(5)
            results.append(to_hex(num))
    return results
