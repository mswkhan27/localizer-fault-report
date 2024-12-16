def determine_season():
    input_str = input("Input the month and day (e.g. January 15): ")
    month, day = input_str.split()
    day = int(day)

    if month in ('January', 'February', 'March'):
        season = 'winter'
    else:
        if month in ('April', 'May', 'June'):
            season = 'spring'
        else:
            if month in ('July', 'August', 'September'):
                season = 'summer'
            else:
                season = 'autumn'

    if (month == 'March') and (day > 21):
        season = 'spring'
    else:
        if (month == 'June') and (day > 21):
            season = 'summer'
        else:
            if (month == 'September') and (day > 21):  
                season = 'autumn'
            else:
                if (month == 'December') and (day > 21):
                    season = 'winter'

    print("Season is", season)

determine_season()
