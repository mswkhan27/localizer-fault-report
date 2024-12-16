def display_type_code(n):
    if n:
        return n
    
def is_side_two_equal_three(type_code):
    if type_code >= 0:
        type_code = type_code + 4 # bug, should be 3
        return type_code

def is_side_one_equal_two(type_code):
    if type_code >= 0:
        type_code = type_code + 1
        return type_code

def is_side_one_equal_three(type_code):
    if type_code >= 0:
        type_code = type_code + 2
        return type_code

def trityp(i, j, k):
    if i == 0 or j == 0 or k == 0:
        type_code = display_type_code(3)
    else:
        type_code = 0
        if i == j:
            type_code = is_side_one_equal_two(type_code)
        if i == k:
            type_code = is_side_one_equal_three(type_code)
        if j == k:
            type_code=is_side_two_equal_three(type_code)
        if type_code == 0:
            if (i + j <= k) or (j + k <= i) or (i + k <= j):
                type_code = display_type_code(4)
            else:
                type_code = display_type_code(1)
        elif type_code > 3:
            type_code = display_type_code(3)
        elif (type_code == 1) and (i + j > k):
            type_code = display_type_code(2)
        elif (type_code == 2) and (i + k > j):
            type_code = display_type_code(2)
        elif (type_code == 3) and (j + k > i):
            type_code = display_type_code(2)
        else:
            type_code = display_type_code(4)

    return type_code