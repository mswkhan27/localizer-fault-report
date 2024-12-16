from src.utils import Count 

import math

def circle_overlap_status(x1, y1, r1, x2, y2, r2):
    Count.incC(9)
    d = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    if d <= r1 - r2:
        Count.incC(1)
        return "C2 is in C1"
    else:
        Count.incC(2)
        if d <= r2 - r1:
            Count.incC(3)
            return "C1 is in C2"
        else:
            Count.incC(4)
            if d < r1 + r2:
                Count.incC(5)
                return "Circumference of C1 and C2 intersect"
            else:
                Count.incC(6)
                if d > r1 + r2:
                    Count.incC(7)
                    return "Circumference of C1 and C2 will touch"
                else:
                    Count.incC(8)
                    return "C1 and C2 do not overlap"
