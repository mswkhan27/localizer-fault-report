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
