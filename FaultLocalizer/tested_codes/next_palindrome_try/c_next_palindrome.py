def next_palindrome(digit_list):
    digit_list = sorted(digit_list)
    n = len(digit_list)
    mid = n // 2
    if n % 2 == 0:
        left_side = digit_list[:mid]
        left_side_reverse = left_side[::-1]
        candidate = left_side + left_side_reverse
    else:
        left_side_reverse = left_side[::-1]
        left_half_end = mid
        right_half_start = mid + 1
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