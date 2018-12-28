

def create_filename(month):
    month = int(month)
    month_name = ''
    if month == 1:
        month_name = 'January'
    elif month == 2:
        month_name = 'February'
    elif month == 3:
        month_name = 'March'
    elif month == 4:
        month_name = 'April'
    elif month == 5:
        month_name = 'May'
    elif month == 6:
        month_name = 'June'
    elif month == 7:
        month_name = 'July'
    elif month == 8:
        month_name = 'August'
    elif month == 9:
        month_name = 'September'
    elif month == 10:
        month_name = 'October'
    elif month == 11:
        month_name = 'November'
    elif month == 12:
        month_name = 'December'

    base_name = '%s_result.xlsx' % month_name
    return base_name