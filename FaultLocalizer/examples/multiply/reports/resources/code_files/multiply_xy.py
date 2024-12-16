def multiply_xy(x, y):
    c[8] += 1
    if x == 0 or y == 0:
        c[1] += 1
        return 0
    rxy = 0
    for i in range(abs(x)):
        c[2] += 1
        if x >= 0:
            c[3] += 1
            rxy = rxy + y
        else:
            c[4] += 1
            rxy = -(rxy + y)
    print("First Two Inputs Prod:",rxy)    
    return rxy
