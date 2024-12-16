c[7] += 1
uMinusOne = u - 1
numerator = uMinusOne
lnTerm = uMinusOne
result = uMinusOne
if v == 0:
    c[1] += 1
    result = 1
else:
    c[2] += 1
    lista = [0, 0]
    if int(v) == v and v > 0:
        c[3] += 1
        result = 1
        for i in range(1, int(v) + 1):
            c[4] += 1
            result *= u
    else:
        c[5] += 1
        uMinusOne = Decimal(u - 1)
        numerator = uMinusOne
        lnTerm = uMinusOne
        result = uMinusOne
        i = 1
        while lnTerm > Decimal(1e-16):
            c[6] += 1
            i += 1
            lnTerm *= uMinusOne * Decimal(-1) / Decimal(i)
            numerator = numerator * Decimal(-1) * uMinusOne
            lnTerm = numerator / Decimal(i)
            result += lnTerm
        result = Decimal(math.exp(v * float(result)))
return result
