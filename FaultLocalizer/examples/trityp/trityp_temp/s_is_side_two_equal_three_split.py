c[19] += 1
if type_code >= 0:
    c[2] += 1
    type_code = type_code + 4 # bug, should be 3
    return type_code
