def is_side_two_equal_three(type_code):
    if type_code >= 0:
        c[2] += 1
        type_code = type_code + 3 # fault 1, was + 3
        return type_code
