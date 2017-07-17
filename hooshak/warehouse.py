from hooshak.modeling import HooshakEntityMixin


class Warehouse:
    def add_entities(self, *entities: HooshakEntityMixin):
        pass

    def add_activities(self, *activities):
        pass

    def app_users(self, *users):
        pass
