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
                month_length = 5
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

def main(input_str):
    # Parse the input string
    try:
        day, month, year = map(int, input_str.split())
    except ValueError:
        raise ValueError("Input must be three integers separated by spaces (day month year).")
    
    # Validate inputs
    if not (1 <= month <= 12):
        raise ValueError("Month must be between 1 and 12.")
    if not (1 <= day <= 31):
        raise ValueError("Day must be between 1 and 31.")
    
    next_year, next_month, next_day = get_next_date(day, month, year)
    return f"{next_day:02d}-{next_month:02d}-{next_year}."

# Example usage
input_str = input("Enter the date (day month year): ")  # e.g., "22 7 2024"
print(main(input_str))
