def next_palindrome(digit_list):
    digit_list = sorted(digit_list)
    n = len(digit_list)
    mid = n // 2
    
    if n % 2 == 0:  # Even-length number
        left_side = digit_list[:mid]
        left_side_reverse = left_side[::-1]
        candidate = left_side + left_side_reverse
    else:  # Odd-length number
        left_side = digit_list[:mid]
        middle = digit_list[mid]
        left_side_reverse = left_side[::-1]
        candidate = left_side + [middle] + left_side_reverse
    
    # If the candidate palindrome is larger than the original, return it
    if candidate > digit_list:
        return candidate
    
    # Increment the left side and adjust if needed
    for i in range(mid - 1, -1, -1):
        if digit_list[i] < 9:
            digit_list[i] += 1
            if i != n - i - 1:
                digit_list[n - i - 1] = digit_list[i]
            return digit_list[:mid] + [digit_list[mid]] * (n % 2) + digit_list[mid - 1::-1]
        digit_list[i] = 0
        digit_list[n - i - 1] = 0

    return [1] + [0] * (n - 1) + [1]



print(next_palindrome([3, 5, 9, 3]))