def next_palindrome(digit_list):
    n = len(digit_list)
    high_mid = n // 2
    low_mid = (n - 1) // 2
    
    while high_mid < n and low_mid >= 0:
        if digit_list[high_mid] == 9:
            digit_list[high_mid] = 0
            digit_list[low_mid] = 0
            high_mid += 1
            low_mid -= 1
        else:
            digit_list[high_mid] += 1
            if low_mid != high_mid:
                digit_list[low_mid] += 1
            break
    
    # If the entire number was made of 9's, we need to handle the carry
    if high_mid == n:
        digit_list = [1] + [0] * (n - 1) + [1]
    
    return digit_list

# Example usage:
digit_list = [1, 2, 9, 4, 8]
print(next_palindrome(digit_list))  # Output: [1, 3, 0, 3, 1]
