c[17] += 1
if year % 400 == 0:
    c[1] += 1
    leap_year = True
else:
    c[2] += 1
    if year % 100 == 0:
        c[3] += 1
        leap_year = False
    else:
        c[4] += 1
        if year % 4 == 0:
            c[5] += 1
            leap_year = True
        else:
            c[6] += 1
            leap_year = False
if month in (1, 3, 5, 7, 8, 10, 12):
    c[7] += 1
    month_length = 31
else:
    c[8] += 1
    if month == 2:
        c[9] += 1
        if leap_year:
            c[10] += 1
            month_length = 29
        else:
            c[11] += 1
            month_length = 5 #bug
    else:
        c[12] += 1
        month_length = 30
if day < month_length:
    c[13] += 1
    day += 1
else:
    c[14] += 1
    day = 1
    if month == 12:
        c[15] += 1
        month = 1
        year += 1
    else:
        c[16] += 1
        month += 1
return day, month, year
