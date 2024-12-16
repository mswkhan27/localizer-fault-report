def next_palindrome(digit_list):
    high_mid = len(digit_list) // 2
    low_mid = (len(digit_list) - 1) // 2
    while high_mid < len(digit_list) and low_mid >= 0:
        if digit_list[high_mid] == 9:
            digit_list[high_mid] = 0
            digit_list[low_mid] = 0
            high_mid += 1
            low_mid -= 1
        else:
            digit_list[high_mid] += 1
            if low_mid != high_mid:
                digit_list[low_mid] += 1
            return digit_list
    return [1] + (len(digit_list) - 1) * [0] + [1]

inputs = [
    [1, 2, 3],  
    [9, 9, 9],  
    [8, 7, 6], 
    [2, 3, 2],  
    [0, 0, 0], 
    [4, 5, 6, 7],  
    [1, 4, 4, 1], 
    [7, 8, 7] ]

print("Testing revised next_palindrome with a mistake:")
for inp in inputs:
    result = next_palindrome(inp.copy())  
    print(f"Input: {inp} -> Output: {result}")