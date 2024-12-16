from src.utils import Count 

def multiply_xy(x, y):
    Count.incC(8)
    if x == 0 or y == 0:
        Count.incC(1)
        return 0
    rxy = 0
    for i in range(abs(x)):
        Count.incC(2)
        if x >= 0:
            Count.incC(3)
            rxy = rxy + y
        else:
            Count.incC(4)
            rxy = -(rxy + y)
    print("First Two Inputs Prod:",rxy)    
    return rxy
