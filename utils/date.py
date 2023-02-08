from datetime import datetime


def string_to_date(s):
    return datetime.strptime(s, '%b %d, %Y')


def date_to_string(d):
    return d.strftime('%b %d, %Y')
