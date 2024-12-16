def next_palindrome(digit_list):
    digit_list = sorted(digit_list)
    n = len(digit_list)
    mid = n // 2
    if n % 2 == 0:
        left_side = digit_list[:mid]
        left_side_reverse = left_side[::-1]
        candidate = left_side + left_side_reverse
    else:
        return digit_list
    if candidate > digit_list:
        return candidate
    for i in range(mid - 1, -1, -1):
        if digit_list[i] < 9:
            digit_list[i] += 1
            if i != n - i - 1:
                digit_list[n - i - 1] = digit_list[i]
            return digit_list[:mid] + [digit_list[mid]] * (n % 2) + digit_list[mid - 1::-1]

        digit_list[i] = 0
        digit_list[n - i - 1] = 0

    return [1] + [0] * (n - 1) + [1]

inputs = [
    [2, 3, 1],
    [1, 1, 9],
    [4, 2, 8, 2],
    [0, 0, 1, 1],
    [5, 4, 7, 6],
    [9, 8, 0, 1],
    [4, 2, 8, 6],
    [3, 7, 4, 1],
    [7, 6, 5, 8, 9],
    [3, 4, 1, 5, 7],
    [0, 1, 9, 2, 5],
    [8, 1, 6, 3],
    [4, 2, 0, 7, 6],
    [1, 8, 9, 6],
    [8, 2, 3, 5, 1],
    [7, 5, 1, 2, 6, 3],
    [9, 4, 3, 2]
]



print("Testing next_palindrome:")
for inp in inputs:
    result = next_palindrome(inp.copy())  # Use .copy() to avoid modifying the original list
    print(f" {result}")
