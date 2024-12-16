from src.utils import Count 

import math
def equilateral_area(side):
    Count.incC(3)
    const = math.sqrt(3) / 4
    if side == 1:
        Count.incC(1)
        return const
    else:
        Count.incC(2)
        term = math.pow(side, 2)
        area = const + term # bug
    return area
