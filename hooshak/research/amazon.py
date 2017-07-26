import os
import csv
import functools
import operator
import random

from hooshak import wise
from hooshak.context import hooshex
from hooshak.modeling import HooshakUserMixin
from hooshak.tools import HTimer

"""

ratings_Movies_and_TV.csv -> ~ 4,600,000 record
ratings_Movies_and_TV.csv -> ~ Unique user number:  2088620
ratings_Movies_and_TV.csv -> ~ Unique entity number: 200941


beautiful_ratings_Movies_and_TV.csv:

    Rows number:          1,932,230
    Unique user number:     139,138
    Unique entity number:   153,436


    first: ['A29X9U79LWG6YT', 'B00JH4SZWK', 4, 1406073600]  --->  Wednesday, July 23, 2014 12:00:00 AM
    last:  ['A1127LKNR08JJK', '630174411X', 4, 879379200]   --->  Thursday, November 13, 1997 12:00:00 AM
    
    Research Items: 1,352,561 (70%) 
    Predict Items:    579,669 (30%) 


"""

class User(HooshakUserMixin):
    def __init__(self, uid):
        self._uid = uid

    def get_hooshak_uid(self):
        return self._uid


# csv_uri = '../../datasource/ratings_Movies_and_TV.csv'
csv_uri = '../../datasource/beautiful_ratings_Movies_and_TV_reverse.csv'
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
            # if row_number == 1000000:
            #     break

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
        print(
            f'Selected index: {selected_index} is: {sorted(user_dict.items(), key=operator.itemgetter(1))[selected_index][1]}')


def check_duplicate_doesnt_exists():
    # TODO: Implement
    pass


def make_beautiful():
    remained_user_list = []
    beautiful_rows = []
    user_dict = {}

    with open('../../datasource/ratings_Movies_and_TV.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=csv_delimiter)
        for row in csv_reader:
            row[2] = int(row[2][0])
            row[3] = int(row[3])
            if row[0] in user_dict:
                user_dict[row[0]].append(row)
            else:
                user_dict[row[0]] = [row]

    print(f'Number of all users: {len(user_dict)}')

    # with open(csv_uri, 'r') as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter=csv_delimiter)
    #     counter = 0
    #     for row in csv_reader:
    #         if row[0] in remained_user_list:
    #             beautiful_rows.append(row)
    #             counter += 1
    #             print(counter)
    #
    # beautiful_rows.sort(key=operator.itemgetter(3), reverse=True)
    beautiful_csv_uri = '../../datasource/beautiful_ratings_Movies_and_TV_reverse.csv'
    #
    # print('Writing...')
    #
    # with open(beautiful_csv_uri, 'w', newline='') as csvfile:
    #     spamwriter = csv.writer(csvfile, delimiter=',',
    #                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     for row in beautiful_rows:
    #         spamwriter.writerow(row)

    beautiful_counter = 0
    for key, value in user_dict.items():
        if len(value) >= 5:
            for row in value:
                beautiful_rows.append(row)
            beautiful_counter += 1
    print(f'Beautiful count: {beautiful_counter}')

    beautiful_rows.sort(key=operator.itemgetter(3), reverse=False)
    print(beautiful_rows[0])
    print(beautiful_rows[-1])

    with open(beautiful_csv_uri, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in beautiful_rows:
            spamwriter.writerow(row)


def seek_and_predict():
    predict_count = 0
    err_sum = 0
    total_err_percent = 0
    last_1000_err = []

    average_err_sum = 0
    average_total_err_percent = 0
    average_last_1000_err = []

    warehouse = hooshex.warehouse
    with open(csv_uri, 'r') as csv_file:
        row_number = 0
        csv_reader = csv.reader(csv_file, delimiter=csv_delimiter)
        for row in csv_reader:
            user_uid = row[0]
            entity_uid = row[1]
            value = row[2]
            timestamp = row[3]

            if row_number > 10000:
                try:
                    average_predict = int(hooshex.cpu.calculate_average_vote(user_uid, entity_uid))
                    raw_predict = hooshex.cpu.calculate_smart_score(user_uid, entity_uid)
                    hooshak_predict = int(raw_predict)
                    # hooshak_predict = 5
                    reality = int(value)
                    # print(f'About {row} in row number : {row_number}')
                    # print(f'Raw predict {raw_predict}')
                    # print(f'Hooshak vs Reality: {hooshak_predict} vs {reality}')
                    # print('\n')

                    predict_count += 1
                    this_err = abs(reality - hooshak_predict)
                    err_sum += this_err

                    last_1000_err.append(this_err)
                    if len(last_1000_err) > 1000:
                        last_1000_err.pop(0)

                    total_err_percent = (err_sum / predict_count) * 25

                    os.system('clear')
                    print(f'average_predict {average_predict}')
                    print(f'hooshak_predict {hooshak_predict}')
                    print(f'reality {reality}')
                    print(f'timestamp {timestamp}')
                    print(f'this_err {this_err}')
                    print(f'predict_count {predict_count}')
                    print(f'err_sum {err_sum}')
                    print(f'total_err_percent {total_err_percent}')
                    print(f'last_10_err {last_1000_err[-10:]}')
                    print(f'last_1000_err_percent {functools.reduce(operator.add, last_1000_err, 1) / 40}')

                    predict_count += 1
                    average_this_err = abs(reality - average_predict)
                    average_err_sum += average_this_err

                    average_last_1000_err.append(average_this_err)
                    if len(average_last_1000_err) > 1000:
                        average_last_1000_err.pop(0)

                    average_total_err_percent = (average_err_sum / predict_count) * 25
                    print(f'\n')
                    print(f'average_this_err {average_this_err}')
                    print(f'average_predict_count {predict_count}')
                    print(f'average_err_sum {average_err_sum}')
                    print(f'average_total_err_percent {average_total_err_percent}')
                    print(f'average_last_10_err {average_last_1000_err[-10:]}')
                    print(f'average_last_1000_err_percent {functools.reduce(operator.add, average_last_1000_err, 1) / 40}')


                except KeyError:
                    # print(f'KeyError: {user_uid} or {entity_uid}')
                    # print('\n')
                    pass
                except TypeError:
                    # print(f'TypeError: {user_uid} or {entity_uid}')
                    # print('\n')
                    pass
                except ZeroDivisionError:
                    # print(f'TypeError: {user_uid} or {entity_uid}')
                    # print('\n')
                    pass

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
            # if row_number == 1000000:
            #     break


if __name__ == '__main__':
    warehouse = hooshex.warehouse

    # calculate_rows()
    # calculate_unique_users()
    # calculate_unique_entities()
    # calculate_user_activities()
    # make_beautiful()

    timer = HTimer()

    # timer.start()
    # read()
    # timer.end_and_print()

    # timer.start()
    # # warehouse.save('../../datasource/ratings_Movies_and_TV.gt')
    # warehouse.save('../../datasource/beautiful_ratings_Movies_and_TV_reverse.gt')
    # timer.end_and_print()

    # timer.start()
    # warehouse.load('../../datasource/ratings_Movies_and_TV.gt')
    # timer.end_and_print()

    # timer.start()
    # find_usable()
    # timer.end_and_print()

    # cpu = hooshex.cpu
    # while True:
    #     inp = input("Type 2 param (separate with `,`)\n").split(',')
    #
    #     result = hooshex.cpu.calculate_smart_score(inp[0], inp[1])
    #     if result and len(result) > 0:
    #         print('%s item %s' % (len(result), int(functools.reduce(operator.add, result, 1) / len(result))))
    #
    #         # print('Hello')

    seek_and_predict()
