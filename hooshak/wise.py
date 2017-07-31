class Wise:
    def __init__(self, warehouse, cpu):
        self.warehouse = warehouse
        self.cpu = cpu

    def learn(self, user_uid: str, entity_uid: str, value: int, timestamp: int):
        try:
            self.warehouse.get_user_v_by_uid(user_uid)
        except KeyError:
            self.warehouse.add_user(user_uid)
        try:
            self.warehouse.get_entity_v_by_uid(entity_uid)
        except KeyError:
            self.warehouse.add_entity(entity_uid)
        self.warehouse.add_activity(user_uid, entity_uid, value, timestamp)

    def predict(self, user_uid, entity_uid, timestamp):

        pass
