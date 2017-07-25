import csv

from hooshak.context import hooshex
from hooshak.modeling import HooshakUserMixin
from hooshak.tools import HTimer


class User(HooshakUserMixin):
    def __init__(self, uid):
        self._uid = uid

    def get_hooshak_uid(self):
        return self._uid


if __name__ == '__main__':

    timer = HTimer()
    csv_uri = '../../datasource/ratings_Movies_and_TV.csv'
    csv_delimiter = ','

    warehouse = hooshex.warehouse

    timer.start()
    with open(csv_uri, 'r') as csv_file:
        row_number = 0

        csv_reader = csv.reader(csv_file, delimiter=csv_delimiter)
        for row in csv_reader:
            user_uid = row[0]
            entity_uid = row[1]
            value = row[1]
            timestamp = row[2]

            if not warehouse.get_user_v_by_uid(user_uid):
                warehouse.add_user(user_uid)
            if not warehouse.get_entity_v_by_uid(entity_uid):
                warehouse.add_entity(entity_uid)
                
            warehouse.add_activity(user_uid, entity_uid, value, timestamp)

            row_number += 1

        print(f'Total rows: {row_number}')

        timer.end_and_print()

    print('Hello')
