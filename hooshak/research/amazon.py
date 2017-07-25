import csv

from hooshak.context import hooshex
from hooshak.modeling import HooshakUserMixin
from hooshak.tools import HTimer


class User(HooshakUserMixin):
    def __init__(self, uid):
        self._uid = uid

    def get_hooshak_uid(self):
        return self._uid


def read():
    csv_uri = '../../datasource/ratings_Movies_and_TV.csv'
    csv_delimiter = ','

    warehouse = hooshex.warehouse

    with open(csv_uri, 'r') as csv_file:
        row_number = 0

        csv_reader = csv.reader(csv_file, delimiter=csv_delimiter)
        for row in csv_reader:
            user_uid = row[0]
            entity_uid = row[1]
            value = row[2]
            timestamp = row[3]

            try:
                warehouse.get_user_v_by_uid(user_uid)
            except KeyError:
                warehouse.add_user(user_uid)

            try:
                warehouse.get_entity_v_by_uid(entity_uid)
            except KeyError:
                warehouse.add_entity(entity_uid)

            warehouse.add_activity(user_uid, entity_uid, int(value[0]), int(timestamp))

            row_number += 1
            if row_number == 100000:
                break

        print(f'Total rows: {row_number}')

if __name__ == '__main__':
    warehouse = hooshex.warehouse

    timer = HTimer()

    # timer.start()
    # read()
    # timer.end_and_print()
    #
    # timer.start()
    # warehouse.save('../../datasource/ratings_Movies_and_TV.gt')
    # timer.end_and_print()

    timer.start()
    warehouse.load('../../datasource/ratings_Movies_and_TV.gt')
    timer.end_and_print()

    print('Hello')
