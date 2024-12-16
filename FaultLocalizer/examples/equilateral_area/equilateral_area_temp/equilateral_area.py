import math
def equilateral_area(side):
    const = math.sqrt(3) / 4
    if side == 1:
        return const
    else:
        term = math.pow(side, 2)
        area = const + term # bug
    return area
