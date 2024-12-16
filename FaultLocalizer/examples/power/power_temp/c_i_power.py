from src.utils import Count 

import math

from decimal import *

def power(u: int, v: int, *args):
    Count.incC(7)
    uMinusOne = u - 1
    numerator = uMinusOne
    lnTerm = uMinusOne
    result = uMinusOne

    if v == 0:
        Count.incC(1)
        result = 1
    else:
        Count.incC(2)
        lista = [0, 0]
        if int(v) == v and v > 0:
            Count.incC(3)
            result = 1
            for i in range(1, int(v) + 1):
                Count.incC(4)
                result *= u
        else:
            Count.incC(5)
            uMinusOne = Decimal(u - 1)
            numerator = uMinusOne
            lnTerm = uMinusOne
            result = uMinusOne
            i = 1
            while lnTerm > Decimal(1e-16):
                Count.incC(6)
                i += 1
                lnTerm *= uMinusOne * Decimal(-1) / Decimal(i)
                numerator = numerator * Decimal(-1) * uMinusOne
                lnTerm = numerator / Decimal(i)
                result += lnTerm

            result = Decimal(math.exp(v * float(result)))
    return result
