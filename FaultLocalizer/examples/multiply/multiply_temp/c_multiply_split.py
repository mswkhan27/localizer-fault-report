from src.utils import Count 

def multiply(x, y, z):
    Count.incC(10)
    print("Inputs: ", x, y, z)
    rxy = multiply_xy(x, y)
    if(rxy==0):
        return 0
    else:
        Count.incC(7)
        rxyz = multiply_rxy_z(rxy, z)
        print("multiply done", rxyz)
    return rxyz
