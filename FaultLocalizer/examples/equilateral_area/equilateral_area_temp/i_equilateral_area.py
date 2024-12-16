import math
def equilateral_area(side):
    c[3] += 1
    const = math.sqrt(3) / 4
    if side == 1:
        c[1] += 1
        return const
    else:
        c[2] += 1
        term = math.pow(side, 2)
        area = const + term # bug
    return area
