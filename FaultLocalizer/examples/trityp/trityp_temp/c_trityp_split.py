from src.utils import Count 

def trityp(i, j, k):
    Count.incC(22)
    if i == 0 or j == 0 or k == 0:
        Count.incC(5)
        type_code = display_type_code(3)
    else:
        Count.incC(6)
        type_code = 0
        if i == j:
            Count.incC(7)
            type_code = is_side_one_equal_two(type_code)
        if i == k:
            Count.incC(8)
            type_code = is_side_one_equal_three(type_code)
        if j == k:
            Count.incC(9)
            type_code=is_side_two_equal_three(type_code)
        if type_code == 0:
            Count.incC(10)
            if (i + j <= k) or (j + k <= i) or (i + k <= j):
                Count.incC(11)
                type_code = display_type_code(4)
            else:
                Count.incC(12)
                type_code = display_type_code(1)
        elif type_code > 3:
            Count.incC(13)
            type_code = display_type_code(3)
        elif (type_code == 1) and (i + j > k):
            Count.incC(14)
            type_code = display_type_code(2)
        elif (type_code == 2) and (i + k > j):
            Count.incC(15)
            type_code = display_type_code(2)
        elif (type_code == 3) and (j + k > i):
            Count.incC(16)
            type_code = display_type_code(2)
        else:
            Count.incC(17)
            type_code = display_type_code(4)
    return type_code
