import time
import re

from sqlalchemy.exc import OperationalError
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException

from db import db_session, Order

TIMEOUT_BETWEEN_PHONES_NORMALIZATION_CYCLES = 5 * 60
TIMEOUT_WHEN_ERROR = 10
TIMEOUT_BETWEEN_TRANSACTIONS = 5


def get_normalized_phone_number(source_phone_number, region='RU'):
    if source_phone_number is None:
        return ''

    cleared_phone_number = ''.join(re.findall(r'\d+', source_phone_number))

    if cleared_phone_number.startswith('8'):
        cleared_phone_number = '{}{}'.format(
            phonenumbers.country_code_for_valid_region(region),
            source_phone_number,
        )
    try:
        return str(
            phonenumbers.parse(
                cleared_phone_number,
                region,
            ).national_number,
        )
    except NumberParseException:
        return ''


def normalize_contact_phones(orders):
    for order in orders:
        order.contact_phone_normalized = get_normalized_phone_number(
            order.contact_phone,
        )
    db_session.commit()


def run_phones_normalization_cycle(count_rows_per_transaction=100):
    while True:
        orders = db_session.query(Order).filter(
            Order.contact_phone_normalized.is_(None),
        ).limit(count_rows_per_transaction).all()

        if not orders:
            break

        normalize_contact_phones(orders)

        time.sleep(TIMEOUT_BETWEEN_TRANSACTIONS)


def main():
    while True:
        try:
            run_phones_normalization_cycle()
        except OperationalError:
            db_session.rollback()
            time.sleep(TIMEOUT_WHEN_ERROR)
            continue
        time.sleep(TIMEOUT_BETWEEN_PHONES_NORMALIZATION_CYCLES)


if __name__ == '__main__':
    main()
