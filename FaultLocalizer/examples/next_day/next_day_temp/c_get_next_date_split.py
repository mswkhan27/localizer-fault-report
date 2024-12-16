from src.utils import Count 

def get_next_date(day, month, year):
    Count.incC(17)
    if year % 400 == 0:
        Count.incC(1)
        leap_year = True
    else:
        Count.incC(2)
        if year % 100 == 0:
            Count.incC(3)
            leap_year = False
        else:
            Count.incC(4)
            if year % 4 == 0:
                Count.incC(5)
                leap_year = True
            else:
                Count.incC(6)
                leap_year = False
    if month in (1, 3, 5, 7, 8, 10, 12):
        Count.incC(7)
        month_length = 31
    else:
        Count.incC(8)
        if month == 2:
            Count.incC(9)
            if leap_year:
                Count.incC(10)
                month_length = 29
            else:
                Count.incC(11)
                month_length = 5 #bug
        else:
            Count.incC(12)
            month_length = 30
    if day < month_length:
        Count.incC(13)
        day += 1
    else:
        Count.incC(14)
        day = 1
        if month == 12:
            Count.incC(15)
            month = 1
            year += 1
        else:
            Count.incC(16)
            month += 1
    return day, month, year
