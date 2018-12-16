import time

from sqlalchemy.exc import OperationalError

from db import db_session, Order

TIMEOUT_BETWEEN_PHONES_NORMALIZATION_CYCLES = 5 * 60
TIMEOUT_WHEN_ERROR = 10


def get_normalized_phone_number(source_phone_number, count_digits=10):
    if source_phone_number is None:
        return ''

    return ''.join(
        [symbol for symbol in source_phone_number if symbol.isdecimal()],
    )[-count_digits:]


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
