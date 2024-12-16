def carry_number(x, y):
    ctr = 0
    z = 0
    if x == 0 and y == 0:
        return 0
    for _ in range(10): 
        z = x % 10 + y % 10 + z
        if z > 9:
            ctr += 1 
            z = 1  
        else:
            z = 0  
        x //= 10
        y //= 10
    return ctr

print(carry_number(786, 457))  # Output: 1 (one carry operation)
print(carry_number(22, 3))      # Output: 0 (no carry operation)
