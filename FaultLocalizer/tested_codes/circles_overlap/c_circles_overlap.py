import math

def circle_overlap_status(x1, y1, r1, x2, y2, r2):
    d = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    if d <= r1 - r2:
        return "C2 is in C1"
    else:
        if d <= r2 - r1:
            return "C1 is in C2"
        else:
            if d < r1 + r2:
                return "Circumference of C1 and C2 intersect"
            else:
                if d == r1 + r2:
                    return "Circumference of C1 and C2 will touch"
                else:
                    return "C1 and C2 do not overlap"

# Main program
print("Input x1, y1, r1, x2, y2, r2:")
inputs = input().split()
x1 = float(inputs[0])
y1 = float(inputs[1])
r1 = float(inputs[2])
x2 = float(inputs[3])
y2 = float(inputs[4])
r2 = float(inputs[5])

result = circle_overlap_status(x1, y1, r1, x2, y2, r2)
print(result)
