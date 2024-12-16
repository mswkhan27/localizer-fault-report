def get_next_date(day, month, year):
    # Determine if it's a leap year
    if year % 400 == 0:
        leap_year = True
    else:
        if year % 100 == 0:
            leap_year = False
        else:
            if year % 4 == 0:
                leap_year = True
            else:
                leap_year = False

    # Determine the length of the month
    if month in (1, 3, 5, 7, 8, 10, 12):
        month_length = 31
    else:
        if month == 2:
            if leap_year:
                month_length = 29
            else:
                month_length = 28
        else:
            month_length = 30

    # Calculate the next day
    if day < month_length:
        day += 1
    else:
        day = 1
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1

    return day, month, year

