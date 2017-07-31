import threading

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

    # Error


    for useruid, entityuid, value, timestamp in AmazonImporter.seek_file():
        if learned_count <= lines_to_learn:
            if not learned_count % 1000:
                print(f'{int(learned_count / lines_to_learn * 100)}% items learned')

            hooshex.wise.learn(user_uid=useruid, entity_uid=entityuid, value=value, timestamp=timestamp)

            if learned_count == lines_to_learn:
                print(f'Learn finished! {learned_count} Item learned.')
                break

            learned_count += 1

        else:
            # It is time to predict!

            hooshak_predict = hooshex.wise.predict(user_uid=useruid, entity_uid=entityuid)





if __name__ == '__main__':
    thread = threading.Thread(target=run, args=())
    thread.daemon = False
    thread.start()
