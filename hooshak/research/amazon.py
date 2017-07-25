import csv
import functools
import operator

from hooshak import wise
from hooshak.context import hooshex
from hooshak.modeling import HooshakUserMixin
from hooshak.tools import HTimer

"""

ratings_Movies_and_TV.csv -> ~ 4,600,000 record
ratings_Movies_and_TV.csv -> ~ Unique user number:  2088620
ratings_Movies_and_TV.csv -> ~ Unique entity number: 200941

"""


class User(HooshakUserMixin):
    def __init__(self, uid):
        self._uid = uid

    def get_hooshak_uid(self):
        return self._uid


csv_uri = '../../datasource/ratings_Movies_and_TV.csv'
csv_delimiter = ','


def read():
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
            if row_number == 1000000:
                break

        print(f'Total rows: {row_number}')


def find_usable():
    with open(csv_uri, 'r') as csv_file:
        row_number = 0
        usable_number = 0
        csv_reader = csv.reader(csv_file, delimiter=csv_delimiter)
        for row in csv_reader:
            if 1000000 < row_number:
                try:
                    hooshex.warehouse.get_user_v_by_uid(row[0])
                    hooshex.warehouse.get_entity_v_by_uid(row[1])
                    print(f'Use this: {row[0]},{row[1]} it should be: {row[2]}')
                    usable_number += 1
                except KeyError:
                    pass
                if usable_number > 10:
                    return
            row_number += 1


def calculate_rows():
    with open(csv_uri, 'r') as csv_file:
        row_number = 0
        csv_reader = csv.reader(csv_file, delimiter=csv_delimiter)
        for row in csv_reader:
            row_number += 1
        print(f'Rows number: {row_number}')


def calculate_unique_users():
    with open(csv_uri, 'r') as csv_file:
        user_list = []
        csv_reader = csv.reader(csv_file, delimiter=csv_delimiter)
        for row in csv_reader:
            user_list.append(row[0])

        print(f'Unique user number: {len(list(set(user_list)))}')


def calculate_unique_entities():
    with open(csv_uri, 'r') as csv_file:
        entity_list = []
        csv_reader = csv.reader(csv_file, delimiter=csv_delimiter)
        for row in csv_reader:
            entity_list.append(row[1])

        print(f'Unique entity number: {len(list(set(entity_list)))}')


def calculate_user_activities():
    with open(csv_uri, 'r') as csv_file:
        user_dict = {}
        csv_reader = csv.reader(csv_file, delimiter=csv_delimiter)
        for row in csv_reader:
            if row[0] in user_dict:
                user_dict.update({row[0]: user_dict[row[0]] + 1})
            else:
                user_dict[row[0]] = 1

        _sum = 0
        for key, value in sorted(user_dict.items(), key=operator.itemgetter(1)):
            # print(f'User: {key} ---- Activity number: {value}')
            _sum += value

        print(f'Sum: {_sum}')

        selected_index = 1900000
        print(f'Selected index: {selected_index} is: {sorted(user_dict.items(), key=operator.itemgetter(1))[selected_index][1]}')


def make_beautiful():
    with open(csv_uri, 'r') as csv_file:
        user_dict = {}
        csv_reader = csv.reader(csv_file, delimiter=csv_delimiter)
        for row in csv_reader:
            if row[0] in user_dict:
                user_dict.update({row[0]: user_dict[row[0]] + 1})
            else:
                user_dict[row[0]] = 1

        remained_user_list = []
        should_delete_number = 1900000
        for key, value in sorted(user_dict.items(), key=operator.itemgetter(1)):
            if should_delete_number < 0:
                remained_user_list.append(key)
            should_delete_number -= 1

        print(f'Number of remained users: {len(remained_user_list)}')

if __name__ == '__main__':
    warehouse = hooshex.warehouse

    # calculate_rows()
    # calculate_unique_users()
    # calculate_unique_entities()
    # calculate_user_activities()



    timer = HTimer()

    # timer.start()
    # read()
    # timer.end_and_print()

    # timer.start()
    # warehouse.save('../../datasource/ratings_Movies_and_TV.gt')
    # timer.end_and_print()

    timer.start()
    warehouse.load('../../datasource/ratings_Movies_and_TV.gt')
    timer.end_and_print()

    timer.start()
    find_usable()
    timer.end_and_print()

    cpu = hooshex.cpu
    while True:
        inp = input("Type 2 param (separate with `,`)\n").split(',')

        result = hooshex.cpu.calculate_smart_score(inp[0], inp[1])
        if result and len(result) > 0:
            print('%s item %s' % (len(result), int(functools.reduce(operator.add, result, 1) / len(result))))

            # print('Hello')
