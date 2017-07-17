import unittest

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
        return self.get_hooshak_to()

    by_id = None
    on_id = None
    value = None


class Location(HooshakEntityMixin):
    id = None
    name = None
    category = None

    def get_hooshak_tags(self):
        return self.id

    def get_hooshak_categories(self):
        return []

    def get_hooshak_uid(self):
        return []


class WarehouseTestCase(BaseHooshakTest):
    def test_warehouse_entity(self):
        entities = []

        for i in range(1000000):
            location = Location()
            location.name = f'location{i}'
            location.id = i
            entities.append(location)

        hooshex.warehouse.add_entities(*entities)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
