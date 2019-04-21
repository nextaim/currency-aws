import date_util
import redshift_manager
import requests
import s3_manager


def get_currency_dynamic(currency_code, start_date, end_date):
    url = 'http://www.cbr.ru/scripts/XML_dynamic.asp'
    payload = {
        'date_req1': date_util.format_date(start_date),
        'date_req2': date_util.format_date(end_date),
        'VAL_NM_RQ': currency_code
    }

    response = requests.get(url, params=payload)
    return response.text


def get_currency_dynamic_reports(currency_codes):
    for key in currency_codes:
        start_date, end_date = get_start_date_and_end_date(key)

        if not start_date or not end_date:
            continue

        report = get_currency_dynamic(currency_codes[key], start_date, end_date)
        if report:
            print('uploading ' + key + ' s3')
            s3_key = generate_s3_key(key, start_date, end_date)
            s3_manager.upload_file(s3_key, report)


def get_start_date_and_end_date(currency):
    current_date = date_util.get_current_date()
    last_date = redshift_manager.get_max_date_from_table(currency + '_dynamic')
    if not last_date:
        start_date = date_util.add_months(current_date, -6)
    elif last_date < current_date:
        start_date = date_util.add_days(last_date, 1)
    else:
        return None

    return start_date, current_date


def generate_s3_key(currency_name, start_date, end_date):
    date_format = "%d%m%Y"
    return "%s/%s_%s" % (currency_name,
                         date_util.format_date(start_date, date_format),
                         date_util.format_date(end_date, date_format))
