import threading

import sys

from hooshak.amazon.calculation import ErrorCalculator
from hooshak.configurations import settings
from hooshak.context import hooshex
from hooshak.amazon.importer import AmazonImporter

"""
We will predict the user's votes and compare it with reality to find out error.
The goal is to finding the algorithm with minimum error.

"""


def run():
    lines_to_learn = settings.amazon.lines_to_learn
    learned_count = 0

    lines_to_predict = settings.amazon.lines_to_predict
    predicted_count = 0

    # Error
    error_calculator = ErrorCalculator()

    for useruid, entityuid, value, timestamp in AmazonImporter.seek_file():
        if learned_count <= lines_to_learn:
            if not learned_count % 1000:
                print(f'{int(learned_count / lines_to_learn * 100)}% items learned')

            hooshex.wise.learn(user_uid=useruid, entity_uid=entityuid, value=value, timestamp=timestamp)

            if learned_count == lines_to_learn:
                print(f'Learn finished! {learned_count} Item learned.')

            learned_count += 1

        elif predicted_count <= lines_to_predict:
            # It is time to predict!

            if not predicted_count % 10:
                print(
                    f'{int(predicted_count / lines_to_predict * 100)}% items predicted '
                    f'with error: {error_calculator.average_percent}'
                )

            hooshak_predict = 4
            # hooshak_predict = hooshex.wise.predict(user_uid=useruid, entity_uid=entityuid)

            error_calculator.append(abs(hooshak_predict - value))

            hooshex.wise.learn(user_uid=useruid, entity_uid=entityuid, value=value, timestamp=timestamp)

            if predicted_count == lines_to_predict:
                print(f'Prediction finished! {predicted_count} Item predicted.')

            predicted_count += 1

        else:
            # Print result:

            print('\n\n\n\n')
            print(f'Total learned items: {learned_count-1}', file=sys.stderr)
            print(f'Total predicted items: {predicted_count-1}', file=sys.stderr)

            print('\n\n')
            print(f'Error total count items: {error_calculator.total_count}')
            print(f'Error total value items: {error_calculator.total_value}')

            print('\n\n')
            print(f'Error average value items: {error_calculator.average_value}')
            print(f'Error average percent items: {error_calculator.average_percent}', file=sys.stderr)

            print('\n\n')
            print(f'Error first 100 items total value items: {error_calculator.first_n_total_value(100)}')
            print(f'Error last 100 items total value items: {error_calculator.last_n_total_value(100)}')
            print('\n')
            print(f'Error first 100 items average value items: {error_calculator.first_n_average_value(100)}')
            print(f'Error last 100 items average value items: {error_calculator.last_n_average_value(100)}')
            print('\n')
            print(f'Error first 100 items average percent items: {error_calculator.first_n_average_percent(100)}',
                  file=sys.stderr)
            print(f'Error last 100 items average percent items: {error_calculator.last_n_average_percent(100)}',
                  file=sys.stderr)

            print('\n\n')
            print(f'Error first 1000 items total value items: {error_calculator.first_n_total_value(1000)}')
            print(f'Error last 1000 items total value items: {error_calculator.last_n_total_value(1000)}')
            print('\n')
            print(f'Error first 1000 items average value items: {error_calculator.first_n_average_value(1000)}')
            print(f'Error last 1000 items average value items: {error_calculator.last_n_average_value(1000)}')
            print('\n')
            print(f'Error first 1000 items average percent items: {error_calculator.first_n_average_percent(1000)}',
                  file=sys.stderr)
            print(f'Error last 1000 items average percent items: {error_calculator.last_n_average_percent(1000)}',
                  file=sys.stderr)

            break


if __name__ == '__main__':
    thread = threading.Thread(target=run, args=())
    thread.daemon = False
    thread.start()
