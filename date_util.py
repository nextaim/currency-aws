import datetime
from dateutil.relativedelta import relativedelta


def get_current_date():
    return datetime.date.today()


def format_date(date, template='%d/%m/%Y'):
    return date.strftime(template)


def add_months(date, month_count):
    return date + relativedelta(months=month_count)


def add_days(date, days_count):
    return date + relativedelta(days=days_count)
