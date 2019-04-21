import os
import psycopg2


def get_connection():
    return psycopg2.connect(
        dbname='currencydb',
        host=os.environ.get('CURRENCY_DB_HOST'),
        port=os.environ.get('CURRENCY_DB_PORT'),
        user=os.environ.get('CURRENCY_DB_USER'),
        password=os.environ.get('CURRENCY_DB_PASSWORD')
    )


def get_max_date_from_table(table):
    query = "SELECT max(date) from %s" % table
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query)
    max_date = cursor.fetchone()

    cursor.close()
    connection.close()

    return max_date[0]
