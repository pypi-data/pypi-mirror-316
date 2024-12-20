import jdatetime
from datetime import datetime, timedelta

def jdatetrunc(variable='day', date_value=datetime.now() ):

    quarter_list = [1, 4, 7, 10]
    if type(date_value) == str:
        date_value_d = datetime.strptime(date_value, '%Y-%m-%d %H:%M:%S')
    else:
        date_value_d = date_value
    jdate_value = jdatetime.datetime.fromgregorian(datetime=date_value_d)
    jdate_value_d = jdate_value
    j_year = jdate_value.year
    j_month = jdate_value.month
    j_day = jdate_value.day
    j_hour = jdate_value.hour
    j_minute = jdate_value.minute
    j_second = jdate_value.second
    match variable:
        case 'year':
            jdate_value_d = jdatetime.datetime(j_year, 1, 1, 0, 0)
        case 'quarter':
            jdate_value_d = jdatetime.datetime(j_year, quarter_list[(j_month - 1) // 3], 1, 0, 0, 0)
        case 'month':
            jdate_value_d = jdatetime.datetime(j_year, j_month, 1, 0, 0, 0)
        case 'week':
            jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, 0, 0, 0) - timedelta(days=jdate_value.weekday())
        case 'day':
            jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, 0, 0, 0)
        case 'hour':
            jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, j_hour, 0, 0)
        case 'minute':
            jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, j_hour, j_minute, 0)
        case 'second':
            jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, j_hour, j_minute, j_second)
        case '_':
            jdate_value_d = jdate_value

    return jdate_value_d.togregorian()
