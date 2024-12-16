from src.utils import Count 

def multiply_rxy_z(rxy, z):
    Count.incC(9)
    if rxy == 0 or z == 0:
        Count.incC(5)
        return 0
    rxyz = 0
    for j in range(abs(z)):
        Count.incC(6)
        rxyz = rxyz + rxy
    print("Three Inputs Prod: ", rxyz)
    return rxyz
