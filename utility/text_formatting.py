from jalali_date import datetime2jalali


def jalali_strftime(input_datetime, output_format='%H:%M %Y/%m/%d'):
    return datetime2jalali(input_datetime).strftime(output_format)
