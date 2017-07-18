import functools
import operator
import os
import random
import re
import unittest

import time

from hooshak.context import hooshex
from hooshak.modeling import HooshakUserMixin, HooshakActivityMixin, HooshakEntityMixin
from hooshak.tests.helper import BaseHooshakTest


class Client(HooshakUserMixin):
    id = None
    name = None

    def get_hooshak_uid(self):
        return self.id


class Like(HooshakActivityMixin):
    def get_hooshak_by(self):
        return self.by_id

    def get_hooshak_value(self):
        return self.value

    def get_hooshak_to(self):
        return self.on_id

    by_id = None
    on_id = None
    value = None


class Location(HooshakEntityMixin):
    id = None
    name = None
    category = None

    def get_hooshak_tags(self):
        return []

    def get_hooshak_categories(self):
        return []

    def get_hooshak_uid(self):
        return self.id


last_time = time.time()


def print_time_offset():
    global last_time
    print(time.time() - last_time)
    last_time = time.time()


class CPUTestCase(BaseHooshakTest):
    def test_cpu_entity(self):

        print_time_offset()
        entities = []
        for i in range(1000):
            location = Location()
            location.name = f'location{i}'
            location.id = i + 10000000
            entities.append(location)
        print_time_offset()
        hooshex.warehouse.add_entities(*entities)

        print_time_offset()
        users = []
        for i in range(1000):
            client = Client()
            client.name = f'client{i}'
            client.id = i + 10000000
            users.append(client)
        print_time_offset()
        hooshex.warehouse.add_users(*users)

        print_time_offset()
        activities = []
        for i in range(100):
            for j in range(100):
                like = Like()
                like.by_id = random.randint(1, 999) + 10000000
                like.on_id = random.randint(1, 999) + 10000000
                like.value = random.randint(1, 99)
                activities.append(like)
        print_time_offset()
        hooshex.warehouse.add_activities(*activities)
        print_time_offset()

        for u in users[:5]:
            for e in entities[:5]:
                result = hooshex.cpu.calculate_smart_score(user=u, entity=e)
                if result and len(result) > 0:
                    print('%s item %s' % (len(result), int(functools.reduce(operator.add, result, 1) / len(result))))

        print_time_offset()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
