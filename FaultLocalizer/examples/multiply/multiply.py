def multiply_xy(x, y):
    if x == 0 or y == 0:
        return 0
    rxy = 0
    for i in range(abs(x)):
        if x >= 0:
            rxy = rxy + y
        else:
            rxy = -(rxy + y)
    print("First Two Inputs Prod:",rxy)    
    return rxy
 
def multiply_rxy_z(rxy, z):
    if rxy == 0 or z == 0:
        return 0
    rxyz = 0
    for j in range(abs(z)):
        rxyz = rxyz + rxy
    print("Three Inputs Prod: ", rxyz)
    return rxyz

def multiply(x, y, z):
    print("Inputs: ", x, y, z)
    rxy = multiply_xy(x, y)
    if(rxy==0):
        return 0
    else:
        rxyz = multiply_rxy_z(rxy, z)
        print("multiply done", rxyz)
    return rxyz
