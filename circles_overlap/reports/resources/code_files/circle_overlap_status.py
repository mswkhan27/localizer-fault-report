def circle_overlap_status(x1, y1, r1, x2, y2, r2):
    c[9] += 1
    d = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    if d <= r1 - r2:
        c[1] += 1
        return "C2 is in C1"
    else:
        c[2] += 1
        if d <= r2 - r1:
            c[3] += 1
            return "C1 is in C2"
        else:
            c[4] += 1
            if d < r1 + r2:
                c[5] += 1
                return "Circumference of C1 and C2 intersect"
            else:
                c[6] += 1
                if d > r1 + r2:
                    c[7] += 1
                    return "Circumference of C1 and C2 will touch"
                else:
                    c[8] += 1
                    return "C1 and C2 do not overlap"
