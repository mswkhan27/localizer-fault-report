def display_type_code(n):
    c[18] += 1
    if n:
        c[1] += 1
        return n
    
def is_side_two_equal_three(type_code):
    c[19] += 1
    if type_code >= 0:
        c[2] += 1
        type_code = type_code + 4 # bug, should be 3
        return type_code

def is_side_one_equal_two(type_code):
    c[20] += 1
    if type_code >= 0:
        c[3] += 1
        type_code = type_code + 1
        return type_code

def is_side_one_equal_three(type_code):
    c[21] += 1
    if type_code >= 0:
        c[4] += 1
        type_code = type_code + 2
        return type_code

def trityp(i, j, k):
    c[22] += 1
    if i == 0 or j == 0 or k == 0:
        c[5] += 1
        type_code = display_type_code(3)
    else:
        c[6] += 1
        type_code = 0
        if i == j:
            c[7] += 1
            type_code = is_side_one_equal_two(type_code)
        if i == k:
            c[8] += 1
            type_code = is_side_one_equal_three(type_code)
        if j == k:
            c[9] += 1
            type_code=is_side_two_equal_three(type_code)
        if type_code == 0:
            c[10] += 1
            if (i + j <= k) or (j + k <= i) or (i + k <= j):
                c[11] += 1
                type_code = display_type_code(4)
            else:
                c[12] += 1
                type_code = display_type_code(1)
        elif type_code > 3:
            c[13] += 1
            type_code = display_type_code(3)
        elif (type_code == 1) and (i + j > k):
            c[14] += 1
            type_code = display_type_code(2)
        elif (type_code == 2) and (i + k > j):
            c[15] += 1
            type_code = display_type_code(2)
        elif (type_code == 3) and (j + k > i):
            c[16] += 1
            type_code = display_type_code(2)
        else:
            c[17] += 1
            type_code = display_type_code(4)

    return type_code
