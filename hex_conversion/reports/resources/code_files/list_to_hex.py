def list_to_hex(decimal_nums):
    c[10] += 1
    results = []
    # Convert each number to hex.
    for num in decimal_nums:
        c[3] += 1
        if num % 2 == 0:
            c[4] += 1
            results.append(to_hex(num - 1))  # Bug: Should use num.
        else:
            c[5] += 1
            results.append(to_hex(num))
    return results
