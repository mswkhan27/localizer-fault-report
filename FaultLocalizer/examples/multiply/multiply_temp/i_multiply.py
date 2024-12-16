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
 
def multiply_rxy_z(rxy, z):
    c[9] += 1
    if rxy == 0 or z == 0:
        c[5] += 1
        return 0
    rxyz = 0
    for j in range(abs(z)):
        c[6] += 1
        rxyz = rxyz + rxy
    print("Three Inputs Prod: ", rxyz)
    return rxyz

def multiply(x, y, z):
    c[10] += 1
    print("Inputs: ", x, y, z)
    rxy = multiply_xy(x, y)
    if(rxy==0):
        return 0
    else:
        c[7] += 1
        rxyz = multiply_rxy_z(rxy, z)
        print("multiply done", rxyz)
    return rxyz
