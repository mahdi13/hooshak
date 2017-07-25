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

    timer.start()
    with open(csv_uri, 'r') as csv_file:
        row_number = 0

        csv_reader = csv.reader(csv_file, delimiter=csv_delimiter)
        for row in csv_reader:
            user_uid = row[0]
            entity_uid = row[1]
            value = row[1]
            timestamp = row[2]

            user = User(user_uid)

            row_number += 1

        print(f'Total rows: {row_number}')

        timer.end_and_print()

    print('Hello')
